from arepo.base import Base
from arepo.mixins import EntityLoaderMixin, AssociationLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy import (Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint,
                        ForeignKeyConstraint)
from sqlalchemy.orm import relationship


class CommitModel(Base, EntityLoaderMixin):
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

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the URL.
        """
        super().__init__(**kwargs)
        assert self.sha is not None, "sha must be provided."
        assert self.repository_id is not None, "repository_id must be provided."

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            self.id = generate_id(f"{self.repository_id}_{self.sha}")


class CommitAssociationModel(Base, AssociationLoaderMixin):
    __tablename__ = "commit_association"
    __table_args__ = (
        ForeignKeyConstraint(('commit_id',), ['commit.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
    )

    commit_id = Column(String, ForeignKey('commit.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)


class CommitFileModel(Base, EntityLoaderMixin):
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

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the URL.
        """
        super().__init__(**kwargs)
        assert self.filename is not None, "filename must be provided."
        assert self.commit_id is not None, "commit_id must be provided."

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            # TODO: probably it should be the sha from the commit instead of the commit_id
            self.id = generate_id(f"{self.commit_id}_{self.filename}")


class CommitParentModel(Base, EntityLoaderMixin):
    __tablename__ = "commit_parent"
    __table_args__ = (
        PrimaryKeyConstraint('commit_id', 'parent_id'),
    )

    commit_id = Column('commit_id', String, ForeignKey('commit.id'))
    parent_id = Column('parent_id', String, ForeignKey('commit.id'))
