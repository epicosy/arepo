import pandas as pd
from pathlib import Path

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint

from arepo.base import Base


class LabelModel(Base):
    __tablename__ = "label"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)


class FunctionModel(Base):
    __tablename__ = "function"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    commit_file_id = Column(String, ForeignKey('commit_file.id'))
    start_line = Column('start_line', Integer, nullable=False)
    start_col = Column('start_col', Integer, nullable=False)
    end_line = Column('end_line', Integer, nullable=False)
    end_col = Column('end_col', Integer, nullable=False)
    size = Column('size', Integer, nullable=False)
    content = Column('content', String, nullable=False)


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
