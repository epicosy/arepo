from arepo.base import Base

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint,
                        ForeignKeyConstraint)
from sqlalchemy.orm import relationship


class CommitModel(Base):
    __tablename__ = "commit"

    id = Column('id', String, primary_key=True)
    sha = Column('sha', String, nullable=False)
    kind = Column('kind', String, nullable=False)
    date = Column('date', DateTime, nullable=True)
    state = Column('state', String, nullable=True)
    author = Column('author', String, nullable=True)
    message = Column('message', String, nullable=True)
    changes = Column('changes', Integer, nullable=True)
    available = Column('available', Boolean, nullable=True)
    additions = Column('additions', Integer, nullable=True)
    deletions = Column('deletions', Integer, nullable=True)
    files_count = Column('files_count', Integer, nullable=True)
    parents_count = Column('parents_count', Integer, nullable=True)
    repository_id = Column(String, ForeignKey('repository.id'))
    files = relationship("CommitFileModel", backref="commit")
    parents = relationship(
        "CommitModel",
        secondary="commit_parent",
        primaryjoin="CommitModel.id==CommitParentModel.commit_id",
        secondaryjoin="CommitModel.id==CommitParentModel.parent_id",
        backref="children"
    )


class CommitAssociationModel(Base):
    __tablename__ = "commit_association"
    __table_args__ = (
        ForeignKeyConstraint(('commit_id',), ['commit.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
    )

    commit_id = Column(String, ForeignKey('commit.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)


class CommitFileModel(Base):
    __tablename__ = "commit_file"

    id = Column('id', String, primary_key=True)
    filename = Column('filename', String, nullable=False)
    additions = Column('additions', Integer, nullable=False)
    deletions = Column('deletions', Integer, nullable=False)
    changes = Column('changes', Integer, nullable=False)
    status = Column('status', String, nullable=False)
    extension = Column('extension', String, nullable=True)
    patch = Column('patch', String, nullable=True)
    raw_url = Column('raw_url', String, nullable=True)
    commit_id = Column(String, ForeignKey('commit.id'))
    diff_blocks = relationship("DiffBlockModel", backref="commit_file")
    functions = relationship("FunctionModel", backref="commit_file")


class CommitParentModel(Base):
    __tablename__ = "commit_parent"
    __table_args__ = (
        PrimaryKeyConstraint('commit_id', 'parent_id'),
    )

    commit_id = Column('commit_id', String, ForeignKey('commit.id'))
    parent_id = Column('parent_id', String, ForeignKey('commit.id'))
