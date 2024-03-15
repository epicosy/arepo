import pytest
from arepo.db import get_in_memory_database, DatabaseConnection


@pytest.fixture(scope="session")
def database_engine():
    return get_in_memory_database()


@pytest.fixture(scope="session")
def database_session(database_engine):
    db = DatabaseConnection("", database_engine)
    with db.get_session() as session:
        yield session
