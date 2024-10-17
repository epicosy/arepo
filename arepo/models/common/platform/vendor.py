from arepo.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class VendorModel(Base):
    __tablename__ = "vendor"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    # TODO: add more fields
    products = relationship("ProductModel", back_populates="vendor")
