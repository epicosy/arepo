from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from arepo.base import Base

change_type = Enum('addition', 'deletion', name='change_type')


class ChangeModel(Base):
    __tablename__ = 'change'
    id = Column(String, primary_key=True)
    line = Column('number', Integer, nullable=False)
    content = Column('content', String, nullable=False)
    start_col = Column(Integer)
    end_col = Column(Integer)
    type = Column('type', change_type)
    diff_block_id = Column(String, ForeignKey('diff_block.id'))


class DiffBlockModel(Base):
    __tablename__ = 'diff_block'
    id = Column(String, primary_key=True)
    order = Column(Integer)
    changes = relationship("ChangeModel", backref="diff_block")
    a_path = Column('a_path', String, nullable=False)
    commit_file_id = Column(String, ForeignKey('commit_file.id'))
