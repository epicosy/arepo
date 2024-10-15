from arepo.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint


class TagModel(Base):
    __tablename__ = "tag"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    references = relationship("ReferenceModel", secondary="reference_tag", backref='tags')


class ReferenceModel(Base):
    __tablename__ = "reference"

    id = Column('id', String, primary_key=True)
    url = Column('url', String, nullable=False)
    sources = relationship("SourceModel", secondary="reference_source", backref='references')


class ReferenceTagModel(Base):
    __tablename__ = 'reference_tag'
    __table_args__ = (
        ForeignKeyConstraint(('reference_id',), ['reference.id']),
        ForeignKeyConstraint(('tag_id',), ['tag.id']),
    )

    reference_id = Column(String, ForeignKey('reference.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)


class ReferenceVulnerabilityModel(Base):
    __tablename__ = "reference_vulnerability"
    __table_args__ = (
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
        ForeignKeyConstraint(('reference_id',), ['reference.id'])
    )

    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    reference_id = Column(String, ForeignKey('reference.id'), primary_key=True)

    # Define the relationships
    vulnerability = relationship("VulnerabilityModel", backref="reference_vulnerabilities")
    reference = relationship("ReferenceModel", backref="reference_vulnerabilities")


class ReferenceSourceModel(Base):
    __tablename__ = "reference_source"
    __table_args__ = (
        ForeignKeyConstraint(('reference_id',), ['reference.id']),
        ForeignKeyConstraint(('source_id',), ['source.id'])
    )

    reference_id = Column(String, ForeignKey('reference.id'), primary_key=True)
    source_id = Column(Integer, ForeignKey('source.id'), primary_key=True)
