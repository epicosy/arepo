from arepo.base import Base
from sqlalchemy import Column, String, ForeignKey, Float, ForeignKeyConstraint


class VulnerabilityCVSS3(Base):
    __tablename__ = 'vulnerability_cvss3'
    __table_args__ = (
        ForeignKeyConstraint(('cvss_id',), ['cvss3.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id'])
    )

    cvss_id = Column(String, ForeignKey('cvss2.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)


class CVSS3Model(Base):
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


# TODO: there must be a better way to handle this
class CVSS3AssociationModel(Base):
    __tablename__ = 'cvss3_association'
    __table_args__ = (
        ForeignKeyConstraint(('cvss_id',), ['cvss3.id']),
        ForeignKeyConstraint(('source_id',), ['source.id']),
        ForeignKeyConstraint(('vulnerability_id',), ['vulnerability.id'])
    )

    cvss_id = Column(String, ForeignKey('cvss3.id'), primary_key=True)
    source_id = Column(String, ForeignKey('source.id'), primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'), primary_key=True)
