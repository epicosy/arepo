import pandas as pd
from pathlib import Path

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint

from arepo.models import Base


class CommitModel(Base):
    __tablename__ = "commit"

    id = Column('id', String, primary_key=True)
    sha = Column('sha', String, nullable=False)
    url = Column('url', String, nullable=False)
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
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'))
    files = relationship("CommitFileModel", backref="commit")


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
    lines = relationship("LineModel", backref="commit_file")


class CommitParentModel(Base):
    __tablename__ = "commit_parent"
    __table_args__ = (
        PrimaryKeyConstraint('commit_id', 'parent_id'),
    )

    commit_id = Column('commit_id', String, ForeignKey('commit.id'))
    parent_id = Column('parent_id', String, ForeignKey('commit.id'))


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


class TopicModel(Base):
    __tablename__ = "topic"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    repositories = relationship("RepositoryModel", secondary="repository_topic", backref='topics')

    @staticmethod
    def populate(tables_path: Path):
        topics_df = pd.read_csv(f'{tables_path}/topics.csv')
        Base.metadata.bind.execute(TopicModel.__table__.insert(), topics_df.to_dict(orient="records"))


class RepositoryTopicModel(Base):
    __tablename__ = 'repository_topic'
    __table_args__ = (
        PrimaryKeyConstraint('repository_id', 'topic_id'),
    )

    repository_id = Column('repository_id', String, ForeignKey('repository.id'))
    topic_id = Column('topic_id', String, ForeignKey('topic.id'))


class RepositoryProductTypeModel(Base):
    __tablename__ = 'repository_product_type'
    __table_args__ = (
        PrimaryKeyConstraint('repository_id', 'product_type_id'),
    )

    repository_id = Column('repository_id', String, ForeignKey('repository.id'))
    product_type_id = Column('product_type_id', Integer, ForeignKey('product_type.id'))
