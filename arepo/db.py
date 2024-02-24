from arepo.utils import populate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database
from arepo.models import Base


class DatabaseConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self._engine = create_engine(self.uri)

        Base.metadata.bind = self._engine

    @staticmethod
    def init(uri: str):
        if not database_exists(uri):
            create_database(url=uri, encoding='utf8')

        engine = create_engine(uri)
        # Create tables
        Base.metadata.create_all(engine)
        populate(engine)

    def get_session(self, scoped: bool = False):
        if scoped:
            return scoped_session(sessionmaker(bind=self._engine))
        else:
            return sessionmaker(bind=self._engine)()
