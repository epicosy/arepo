from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint

from arepo.models import Base


class LineModel(Base):
    __tablename__ = "line"

    id = Column('id', String, primary_key=True)
    number = Column('number', Integer, nullable=False)
    content = Column('content', String, nullable=False)
    commit_file_id = Column(String, ForeignKey('commit_file.id'))


class LabelModel(Base):
    __tablename__ = "label"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)


class LineLabelModel(Base):
    __tablename__ = "line_label"
    __table_args__ = (
        PrimaryKeyConstraint('line_id', 'label_id'),
    )

    line_id = Column('line_id', String, ForeignKey('line.id'))
    label_id = Column('label_id', Integer, ForeignKey('label.id'))


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
