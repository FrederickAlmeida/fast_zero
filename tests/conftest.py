import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine  # , select
from sqlalchemy.orm import sessionmaker

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Base, User


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # cria um mecanismo SQLite em memoria, para criar uma sessao
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # cria todas as tabelas do db antes que cada teste use a fixture
    Base.metadata.create_all(engine)

    # cria uma fabrica de sessoes para criar sessoes para os testes
    Session = sessionmaker(bind=engine)

    # fornece uma instancia de session que sera injetada em cada teste que
    #  solicite a fixture, que sera usada para interagir com o banco de dados
    yield Session()
    # apos o teste usar a fixture, todas as tabelas serao eliminadas,
    # garantindo que cada teste seja executado em um banco de dados limpo
    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
