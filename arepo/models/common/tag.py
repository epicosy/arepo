from arepo.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint


class TagModel(Base):
    __tablename__ = "tag"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)

    associations = relationship(
        "TagAssociationModel",
        back_populates='tag'
    )


class TagAssociationModel(Base):
    __tablename__ = 'tag_association'
    __table_args__ = (
        ForeignKeyConstraint(('tag_id',), ['tag.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('reference_id',), ['reference.id']),
    )

    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
    reference_id = Column(String, ForeignKey('reference.id'), primary_key=True)

    tag = relationship("TagModel", back_populates="associations")
    source = relationship("SourceModel", back_populates="tags")
    reference = relationship("ReferenceModel", back_populates="tags")

