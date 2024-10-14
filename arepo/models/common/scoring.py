from arepo.base import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, PrimaryKeyConstraint


class CVSS3SourceModel(Base):
    __tablename__ = 'cvss3_source'
    __table_args__ = (
        PrimaryKeyConstraint('cvss', 'source_id'),
    )

    cvss = Column('cvss', String, ForeignKey('cvss3.id'))
    source_id = Column('source_id', Integer, ForeignKey('source.id'))


class CVSS2SourceModel(Base):
    __tablename__ = 'cvss2_source'
    __table_args__ = (
        PrimaryKeyConstraint('cvss', 'source_id'),
    )

    cvss = Column('cvss', String, ForeignKey('cvss2.id'))
    source_id = Column('source_id', Integer, ForeignKey('source.id'))


# class VulnerabilityCVSS3(Base):
#     __tablename__ = 'vulnerability_cvss3'
#     __table_args__ = (
#         PrimaryKeyConstraint('vulnerability_id', 'cvss3_id'),
#     )

#     vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'), primary_key=True)
#     cvss3_id = Column('cvss3_id', String, ForeignKey('cvss3.id'), primary_key=True)


class CVSS3Model(Base):
    __tablename__ = "cvss3"

    id = Column(String, primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'))
    # cve_id =  Column('cve_id',  String)
    # source =  relationship("source", backref="vulnerability_cvss3")
    type = Column('type', String, nullable=True)  # whether the organization is a primary or secondary source
    cvssData = Column('cvssData', String, nullable=True)
    exploitabilityScore = Column('exploitabilityScore', Float, nullable=True)
    impactScore = Column('impactScore', Float, nullable=True)
    cvssData_version = Column('cvssData_version', String, nullable=True)
    cvssData_vectorString = Column('cvssData_vectorString', String, nullable=True)
    cvssData_attackVector = Column('cvssData_attackVector', String, nullable=True)
    cvssData_attackComplexity = Column('cvssData_attackComplexity', String, nullable=True)
    cvssData_privilegesRequired = Column('cvssData_privilegesRequired', String, nullable=True)
    cvssData_userInteraction = Column('cvssData_userInteraction', String, nullable=True)
    cvssData_scope = Column('cvssData_scope', String, nullable=True)
    cvssData_confidentialityImpact = Column('cvssData_confidentialityImpact', String, nullable=True)
    cvssData_integrityImpact = Column('cvssData_integrityImpact', String, nullable=True)
    cvssData_availabilityImpact = Column('cvssData_availabilityImpact', String, nullable=True)
    cvssData_baseScore = Column('cvssData_baseScore', Float, nullable=True)
    cvssData_baseSeverity = Column('cvssData_baseSeverity', String, nullable=True)
    # cvss3 =  relationship('cvss3', secondary="cvss3_source", backref='cvss3')


# class VulnerabilityCVSS2( Base):
#     __tablename__ = 'vulnerability_cvss2'
#     __table_args__ = (
#          PrimaryKeyConstraint('vulnerability_id', 'cvss2_id'),
#     )

#     vulnerability_id =  Column('vulnerability_id',  String,  ForeignKey('vulnerability.id'), primary_key=True)
#     cvss2_id =  Column('cvss2_id',  String,  ForeignKey('cvss2.id'), primary_key=True)


class CVSS2Model(Base):
    __tablename__ = "cvss2"

    id = Column(String, primary_key=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'))
    # cve_id =  Column('cve_id',  String)
    # source =  relationship("source", backref="vulnerability_cvss2")
    type = Column('type', String, nullable=True)
    # CVSSv2 Specific Columns
    cvssData_version = Column('cvssData_version', String, nullable=True)
    cvssData_vectorString = Column('cvssData_vectorString', String, nullable=True)
    cvssData_accessVector = Column('cvssData_accessVector', String, nullable=True)
    cvssData_accessComplexity = Column('cvssData_accessComplexity', String, nullable=True)
    cvssData_authentication = Column('cvssData_authentication', String, nullable=True)
    cvssData_confidentialityImpact = Column('cvssData_confidentialityImpact', String, nullable=True)
    cvssData_integrityImpact = Column('cvssData_integrityImpact', String, nullable=True)
    cvssData_availabilityImpact = Column('cvssData_availabilityImpact', String, nullable=True)
    cvssData_baseScore = Column('cvssData_baseScore', Float, nullable=True)
    baseSeverity = Column('baseSeverity', String, nullable=True)
    exploitabilityScore = Column('exploitabilityScore', Float, nullable=True)
    impactScore = Column('impactScore', Float, nullable=True)
    # Additional attributes
    acInsufInfo = Column('acInsufInfo', Boolean, nullable=True)
    obtainAllPrivilege = Column('obtainAllPrivilege', Boolean, nullable=True)
    obtainUserPrivilege = Column('obtainUserPrivilege', Boolean, nullable=True)
    obtainOtherPrivilege = Column('obtainOtherPrivilege', Boolean, nullable=True)
    userInteractionRequired = Column('userInteractionRequired', Boolean, nullable=True)
    # cvss2 =  relationship('cvss2', secondary="cvss2_source", backref='cvss2')


class SourceModel(Base):
    __tablename__ = "source"
    id = Column('id', Integer, primary_key=True)  # whether auto increament
    name = Column('name', String)
    link = Column('link', String, nullable=True)

    # vulnerabilities =  relationship('Vulnerability', secondary="vulnerability_cwe", backref='cwes')
