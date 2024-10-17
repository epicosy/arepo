from arepo.base import Base

from sqlalchemy import Column, String


class SourceModel(Base):
    __tablename__ = "source"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False)
