from arepo.base import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship


class RepositoryModel(Base):
    __tablename__ = "repository"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    owner = Column('owner', String, nullable=False)
    available = Column('available', Boolean, nullable=True)
    description = Column('description', String, nullable=True)
    language = Column('language', String, nullable=True)
    size = Column('size', Integer, nullable=True)
    watchers = Column('watchers', Integer, nullable=True)
    forks = Column('forks', Integer, nullable=True)
    stargazers = Column('stargazers', Integer, nullable=True)
    commits_count = Column('commits_count', Integer, nullable=True)
    commits = relationship("CommitModel", backref="repository")

    def __repr__(self):
        return f"<Repository {self.owner}/{self.name}>"


class RepositoryAssociationModel(Base):
    __tablename__ = "repository_association"
    __table_args__ = (
        ForeignKeyConstraint(('repository_id',), ['repository.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
    )

    repository_id = Column(String, ForeignKey('repository.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
