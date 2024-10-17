from arepo.base import Base

from sqlalchemy import Column, Integer, String


class SourceModel(Base):
    __tablename__ = "source"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False)
