from arepo.utils.misc import generate_id

from arepo.base import Base
from arepo.mixins import EntityLoaderMixin, AssociationLoaderMixin

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, ForeignKeyConstraint


class ReferenceModel(Base, EntityLoaderMixin):
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

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the URL.
        """
        super().__init__(**kwargs)
        assert self.url is not None, "URL must be provided."

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            self.id = generate_id(self.url)


class ReferenceAssociationModel(Base, AssociationLoaderMixin):
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
