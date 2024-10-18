from arepo.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, ForeignKeyConstraint


class ReferenceModel(Base):
    __tablename__ = "reference"

    id = Column('id', String, primary_key=True)
    url = Column('url', String, nullable=False)

    # Relationship to ReferenceAssociationModel
    associations = relationship(
        'ReferenceAssociationModel',
        back_populates='reference'
    )

    tags = relationship(
        'TagAssociationModel',
        back_populates='reference'
    )


class ReferenceAssociationModel(Base):
    __tablename__ = "reference_association"
    __table_args__ = (
        ForeignKeyConstraint(('reference_id',), ['reference.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id']),
    )

    reference_id = Column(String, ForeignKey('reference.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)

    # Define the relationships
    vulnerability = relationship("VulnerabilityModel", back_populates="references")
    reference = relationship("ReferenceModel", back_populates="associations")
    source = relationship("SourceModel", back_populates="references")
