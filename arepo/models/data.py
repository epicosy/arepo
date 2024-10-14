from arepo.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Boolean, Float


class DatasetModel(Base):
    __tablename__ = "dataset"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=True)
    vulnerabilities = relationship("VulnerabilityModel", secondary="dataset_vulnerability")

    def __len__(self):
        return len(self.vulnerabilities)


class DatasetVulnerabilityModel(Base):
    __tablename__ = 'dataset_vulnerability'
    __table_args__ = (
        PrimaryKeyConstraint('dataset_id', 'vulnerability_id'),
    )

    dataset_id = Column('dataset_id', Integer, ForeignKey('dataset.id'))
    vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'))


class ProfileModel(Base):
    __tablename__ = "profile"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    has_code = Column('has_code', Boolean, nullable=False)
    has_exploit = Column('has_exploit', Boolean, nullable=False)
    has_advisory = Column('has_advisory', Boolean, nullable=False)
    single_commit = Column('single_commit', Boolean, nullable=False)
    start_year = Column('start_year', Integer, nullable=False)
    end_year = Column('end_year', Integer, nullable=True)
    start_score = Column('start_score', Float, nullable=False)
    end_score = Column('end_score', Float, nullable=False)
    min_changes = Column('min_changes', Integer, nullable=False)
    max_changes = Column('max_changes', Integer, nullable=True)
    min_files = Column('min_files', Integer, nullable=False)
    max_files = Column('max_files', Integer, nullable=True)
    # TODO: make it a relationship to hold more extensions
    extension = Column('extension', String, nullable=True)
    # TODO: should include the size / count


class ProfileCWEModel(Base):
    __tablename__ = 'profile_cwe'
    __table_args__ = (
        PrimaryKeyConstraint('profile_id', 'cwe_id'),
    )

    profile_id = Column('profile_id', Integer, ForeignKey('profile.id'))
    cwe_id = Column('cwe_id', Integer, ForeignKey('cwe.id'))


class CompletionModel(Base):
    # TODO: move this model to a different place
    __tablename__ = "completion"

    id = Column('id', String, primary_key=True)
    object = Column('object', String, nullable=False)
    created = Column('created', Integer, nullable=False)
    model = Column('model', String, nullable=False)
    prompt = Column('prompt', String, nullable=False)
    completion = Column('completion', String, nullable=False)
    finish_reason = Column('finish_reason', String, nullable=False)
    prompt_tokens = Column('prompt_tokens', Integer, nullable=False)
    completion_tokens = Column('completion_tokens', Integer, nullable=False)
    total_tokens = Column('total_tokens', Integer, nullable=False)


class WeaknessModel(Base):
    # TODO: move this model to a different place
    __tablename__ = "weakness"

    id = Column('id', Integer, primary_key=True)
    tuple = Column('tuple', String, nullable=True)
    vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'))
    # TODO: there should be a table to map the Weakness to the Completion table
    completion_id = Column('completion_id', String, ForeignKey('completion.id'))

