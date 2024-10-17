from arepo.base import Base

from sqlalchemy import Column, String, ForeignKey, Boolean, Float, ForeignKeyConstraint


class CVSS2Model(Base):
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


# TODO: there must be a better way to handle this
class CVSS2AssociationModel(Base):
    __tablename__ = 'cvss2_association'
    __table_args__ = (
        ForeignKeyConstraint(('cvss_id',), ['cvss2.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id'])
    )

    cvss_id = Column(String, ForeignKey('cvss2.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
