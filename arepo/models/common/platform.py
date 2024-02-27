from arepo.models import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, PrimaryKeyConstraint


class ConfigurationModel(Base):
    __tablename__ = "configuration"

    id = Column('id', String, primary_key=True)
    vulnerable = Column('vulnerable', Boolean, nullable=True)
    part = Column('part', String, nullable=False)
    version = Column('version', String, nullable=True)
    update = Column('update', String, nullable=True)
    edition = Column('edition', String, nullable=True)
    language = Column('language', String, nullable=True)
    sw_edition = Column('sw_edition', String, nullable=True)
    target_sw = Column('target_sw', String, nullable=True)
    target_hw = Column('target_hw', String, nullable=True)
    other = Column('other', String, nullable=True)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'))
    vendor_id = Column(String, ForeignKey('vendor.id'))
    product_id = Column(String, ForeignKey('product.id'))


class VendorModel(Base):
    __tablename__ = "vendor"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    products = relationship("ProductModel", backref="vendor")


class ProductModel(Base):
    __tablename__ = "product"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    vendor_id = Column(String, ForeignKey('vendor.id'))
    product_type_id = Column(Integer, ForeignKey('product_type.id'))
    configurations = relationship("ConfigurationModel", backref="product")


class ProductTypeModel(Base):
    __tablename__ = "product_type"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    products = relationship("ProductModel", backref="product_type")


class ConfigurationVulnerabilityModel(Base):
    __tablename__ = 'configuration_vulnerability'
    __table_args__ = (
        PrimaryKeyConstraint('configuration_id', 'vulnerability_id'),
    )

    configuration_id = Column('configuration_id', String, ForeignKey('configuration.id'))
    vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'))
