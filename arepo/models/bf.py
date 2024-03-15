from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from arepo.base import Base


class OperationModel(Base):
    __tablename__ = "operation"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    cwes = relationship('CWEModel', secondary="cwe_operation", backref='operations')


class PhaseModel(Base):
    __tablename__ = "phase"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    acronym = Column('acronym', String, nullable=False)
    url = Column('url', String, nullable=True)
    cwes = relationship('CWEModel', secondary="cwe_phase", backref='phases')


class BFClassModel(Base):
    __tablename__ = "bf_class"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    url = Column('url', String, nullable=True)
    cwes = relationship('CWEModel', secondary="cwe_bf_class", backref='bf_classes')
