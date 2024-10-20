from arepo.base import Base
from arepo.mixins import EntityLoaderMixin, AssociationLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy import Column, String, ForeignKey, Boolean, Float, ForeignKeyConstraint
from sqlalchemy.orm import relationship


class CVSS2Model(Base, EntityLoaderMixin):
    __tablename__ = "cvss2"

    id = Column(String, primary_key=True)
    vector_string = Column('vector_string', String)
    access_vector = Column('access_vector', String)
    access_complexity = Column('access_complexity', String)
    authentication = Column('authentication', String)
    confidentiality_impact = Column('confidentiality_impact', String)
    integrity_impact = Column('integrity_impact', String)
    availability_impact = Column('availability_impact', String)
    base_severity = Column('base_severity', String, nullable=True)
    base_score = Column('base_score', Float, nullable=True)
    exploitability_score = Column('exploitability_score', Float, nullable=True)
    impact_score = Column('impact_score', Float, nullable=True)
    # Additional attributes
    ac_insuf_info = Column('ac_insuf_info', Boolean, nullable=True)
    obtain_all_privilege = Column('obtain_all_privilege', Boolean, nullable=True)
    obtain_user_privilege = Column('obtain_user_privilege', Boolean, nullable=True)
    obtain_other_privilege = Column('obtain_other_privilege', Boolean, nullable=True)
    user_interaction_required = Column('user_interaction_required', Boolean, nullable=True)
    # type = Column('type', String, nullable=True)  # TODO: to be added later
    # version = Column('version', String, nullable=True)  # TODO: put back if needed

    associations = relationship(
        "CVSS2AssociationModel",
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
class CVSS2AssociationModel(Base, AssociationLoaderMixin):
    __tablename__ = 'cvss2_association'
    __table_args__ = (
        ForeignKeyConstraint(('cvss_id',), ['cvss2.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id'])
    )

    cvss_id = Column(String, ForeignKey('cvss2.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)

    cvss = relationship("CVSS2Model", back_populates="associations")
    source = relationship("SourceModel", back_populates="cvss2")
    vulnerability = relationship("VulnerabilityModel", back_populates="cvss2")
