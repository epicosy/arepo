from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from arepo.base import Base
from arepo.utils.misc import generate_id
from arepo.mixins import EntityLoaderMixin


change_type = Enum('addition', 'deletion', name='change_type')


class ChangeModel(Base, EntityLoaderMixin):
    __tablename__ = 'change'
    id = Column(String, primary_key=True)
    line = Column('number', Integer, nullable=False)
    content = Column('content', String, nullable=False)
    start_col = Column(Integer)
    end_col = Column(Integer)
    type = Column('type', change_type)
    diff_block_id = Column(String, ForeignKey('diff_block.id'))

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from attributes.
        """
        super().__init__(**kwargs)
        assert self.diff_block_id is not None, "diff_block_id must be provided."
        assert self.type is not None, "type must be provided."
        assert self.line is not None, "line must be provided."
        assert self.start_col is not None, "start_col must be provided."

        if self.id is None:
            self.id = generate_id(f"{self.diff_block_id}_{self.type}_{self.line}_{self.start_col}")


class DiffBlockModel(Base, EntityLoaderMixin):
    __tablename__ = 'diff_block'
    id = Column(String, primary_key=True)
    order = Column(Integer)
    changes = relationship("ChangeModel", backref="diff_block")
    a_path = Column('a_path', String, nullable=False)
    commit_file_id = Column(String, ForeignKey('commit_file.id'))

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from attributes.
        """
        super().__init__(**kwargs)
        assert self.commit_file_id is not None, "commit_file_id must be provided."
        assert self.a_path is not None, "a_path must be provided."
        assert self.order is not None, "order must be provided."

        if self.id is None:
            self.id = generate_id(f"{self.commit_file_id}_{self.a_path}_{self.order}")
