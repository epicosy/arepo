from arepo.base import Base
from arepo.utils.misc import generate_id
from arepo.mixins import EntityLoaderMixin, AssociationLoaderMixin

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship


class RepositoryModel(Base, EntityLoaderMixin):
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

    def has_commits(self, available: bool = False, kind: str = None, has_files: bool = False,
                    has_parents: bool = False):
        """
            check if repo has commits

            :param available: flag to check if the commit is available
            :param kind: kind of commit
            :param has_files: flag to check if the commit has files
            :param has_parents: flag to check if the commit has parents

            :return:
        """

        if len(self.commits) == 0:
            return False

        commits = []

        for c in self.commits:
            # TODO: check for files and parents to avoid mismatches between count and actual entries
            if available and not c.available:
                continue

            if kind and c.kind != kind:
                continue

            if has_files and len(c.files) == 0:
                continue

            if has_parents and len(c.parents) == 0:
                continue

            commits.append(c)

        return len(commits) > 0

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the URL.
        """
        super().__init__(**kwargs)
        assert self.name is not None, "name must be provided."
        assert self.owner is not None, "owner must be provided."

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            self.id = generate_id(f"{self.owner}/{self.name}")

    def __repr__(self):
        return f"<Repository {self.owner}/{self.name}>"


class RepositoryAssociationModel(Base, AssociationLoaderMixin):
    __tablename__ = "repository_association"
    __table_args__ = (
        ForeignKeyConstraint(('repository_id',), ['repository.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
    )

    repository_id = Column(String, ForeignKey('repository.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
