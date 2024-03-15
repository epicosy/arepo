from arepo.utils import populate

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from arepo.base import Base


class DatabaseConnection:
    def __init__(self, uri: str, engine: Engine = None):
        self.uri = uri if engine is None else engine.url
        self._engine = create_engine(self.uri) if engine is None else engine
        self._session_maker = sessionmaker(bind=self._engine)
        Base.metadata.bind = self._engine

        # db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        # Base.query = db_session.query_property()

    @staticmethod
    def init(uri: str):
        if not database_exists(uri):
            create_database(url=uri, encoding='utf8')

        engine = create_engine(uri)
        # Create tables
        Base.metadata.create_all(engine)
        populate(engine)

        return engine

    def get_session(self, scoped: bool = False):
        if scoped:
            db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))
            Base.query = db_session.query_property()
            return db_session
        else:
            return self._session_maker()


def get_in_memory_database() -> Engine:
    """
        This function initializes an in memory database and returns its engine.
    :return:
    """

    db_uri = "sqlite:///:memory:"
    engine = DatabaseConnection.init(db_uri)
    print('Database initialized.')
    print('engine:', engine)

    return engine
