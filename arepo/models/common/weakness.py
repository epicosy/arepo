from arepo.base import Base

from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship


class AbstractionModel(Base):
    __tablename__ = "abstraction"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    cwes = relationship('CWEModel', backref='abstraction')


class GroupingModel(Base):
    __tablename__ = "grouping"
    __table_args__ = (
        PrimaryKeyConstraint('parent_id', 'child_id'),
    )

    parent_id = Column('parent_id', Integer, ForeignKey('cwe.id'))
    child_id = Column('child_id', Integer, ForeignKey('cwe.id'))


class CWEModel(Base):
    __tablename__ = "cwe"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    url = Column('url', String, nullable=False)
    abstraction_id = Column(Integer, ForeignKey('abstraction.id'))
    vulnerabilities = relationship('VulnerabilityModel', secondary="vulnerability_cwe", backref='cwes')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'url': self.url, 'abstraction_id': self.abstraction_id}


class CWEOperationModel(Base):
    __tablename__ = "cwe_operation"
    __table_args__ = (
        ForeignKeyConstraint(('cwe_id',), ['cwe.id']),
        ForeignKeyConstraint(('operation_id',), ['operation.id'])
    )

    cwe_id = Column(Integer, ForeignKey('cwe.id'), primary_key=True)
    operation_id = Column(Integer, ForeignKey('operation.id'), primary_key=True)


class CWEPhaseModel(Base):
    __tablename__ = "cwe_phase"
    __table_args__ = (
        ForeignKeyConstraint(('cwe_id',), ['cwe.id']),
        ForeignKeyConstraint(('phase_id',), ['phase.id']),
    )

    cwe_id = Column(Integer, ForeignKey('cwe.id'), primary_key=True)
    phase_id = Column(Integer, ForeignKey('phase.id'), primary_key=True)


class CWEBFClassModel(Base):
    __tablename__ = "cwe_bf_class"
    __table_args__ = (
        ForeignKeyConstraint(('cwe_id',), ['cwe.id']),
        ForeignKeyConstraint(('bf_class_id',), ['bf_class.id']),
    )

    cwe_id = Column(Integer, ForeignKey('cwe.id'), primary_key=True)
    bf_class_id = Column(Integer, ForeignKey('bf_class.id'), primary_key=True)
