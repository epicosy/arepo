from arepo.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer


class ProductModel(Base):
    __tablename__ = "product"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    part = Column('part', String, nullable=False)
    vendor_id = Column(String, ForeignKey('vendor.id'), nullable=False)
    # TODO: add more fields
    vendor = relationship("VendorModel", back_populates="products")
    cpes = relationship("CPEModel", back_populates="product")
