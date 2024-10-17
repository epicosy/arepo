from arepo.base import Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class ConfigurationModel(Base):
    __tablename__ = "configuration"

    id = Column('id', String, primary_key=True)
    vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'), nullable=False)
    operator = Column('operator', String, nullable=True)
    is_vulnerable = Column('is_vulnerable', Boolean, nullable=True)
    is_multi_component = Column('is_multi_component', Boolean, nullable=True)
    is_platform_specific = Column('is_platform_specific', Boolean, nullable=True)

    nodes = relationship("NodeModel", back_populates="configuration")


class NodeModel(Base):
    __tablename__ = "node"

    id = Column('id', String, primary_key=True)
    configuration_id = Column(String, ForeignKey('configuration.id'), nullable=False)
    operator = Column('operator', String, nullable=False)
    negate = Column('negate', Boolean, nullable=False)
    is_vulnerable = Column('is_vulnerable', Boolean, nullable=True)
    is_multi_component = Column('is_multi_component', Boolean, nullable=True)
    is_context_dependent = Column('is_context_dependent', Boolean, nullable=True)

    configuration = relationship("ConfigurationModel", back_populates="nodes")
    cpe_matches = relationship("CPEMatchModel", back_populates="node")
