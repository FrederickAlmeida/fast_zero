import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine  # , select
from sqlalchemy.orm import sessionmaker

from fast_zero.app import app
from fast_zero.models import Base


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # cria um mecanismo SQLite em memoria, para criar uma sessao
    engine = create_engine('sqlite:///:memory:')
    # cria uma fabrica de sessoes para criar sessoes para os testes
    Session = sessionmaker(bind=engine)
    # cria todas as tabelas do db antes que cada teste use a fixture
    Base.metadata.create_all(engine)
    # fornece uma instancia de session que sera injetada em cada teste que
    #  solicite a fixture, que sera usada para interagir com o banco de dados
    yield Session()
    # apos o teste usar a fixture, todas as tabelas serao eliminadas,
    # garantindo que cada teste seja executado em um banco de dados limpo
    Base.metadata.drop_all(engine)
