from arepo.base import Base
from arepo.mixins import EntityLoaderMixin, AssociationLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Float, ForeignKeyConstraint


class CVSS3Model(Base, EntityLoaderMixin):
    __tablename__ = "cvss3"

    id = Column(String, primary_key=True)
    version = Column('version', String)
    vector_string = Column('vector_string', String)
    attack_vector = Column('attack_vector', String)
    attack_complexity = Column('attack_complexity', String)
    privileges_required = Column('privileges_required', String)
    user_interaction = Column('user_interaction', String)
    scope = Column('scope', String)
    confidentiality_impact = Column('confidentiality_impact', String)
    integrity_impact = Column('integrity_impact', String)
    availability_impact = Column('availability_impact', String)
    base_severity = Column('base_severity', String, nullable=True)
    base_score = Column('base_score', Float, nullable=True)
    exploitability_score = Column('exploitability_score', Float, nullable=True)
    impact_score = Column('impact_score', Float, nullable=True)
    # type = Column('type', String, nullable=True)  # TODO: to be added later

    associations = relationship(
        "CVSS3AssociationModel",
        back_populates="cvss"
    )

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the columns.
        """
        super().__init__(**kwargs)

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            # Get only the defined attributes from the class using __table__.columns
            attributes = {
                col.name: str(getattr(self, col.name)) for col in self.__table__.columns
                if getattr(self, col.name) is not None
            }

            # Create a string representation of the attributes sorted by key
            sorted_attributes_str = ''.join(f"{key}={value}" for key, value in sorted(attributes.items()))

            self.id = generate_id(sorted_attributes_str)


# TODO: there must be a better way to handle this
class CVSS3AssociationModel(Base, AssociationLoaderMixin):
    __tablename__ = 'cvss3_association'
    __table_args__ = (
        ForeignKeyConstraint(('cvss_id',), ['cvss3.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id'])
    )

    cvss_id = Column(String, ForeignKey('cvss3.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)

    cvss = relationship("CVSS3Model", back_populates="associations")
    source = relationship("SourceModel", back_populates="cvss3")
    vulnerability = relationship("VulnerabilityModel", back_populates="cvss3")

