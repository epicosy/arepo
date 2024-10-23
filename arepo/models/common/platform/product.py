from arepo.base import Base
from arepo.mixins import EntityLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class ProductModel(Base, EntityLoaderMixin):
    __tablename__ = "product"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    part = Column('part', String, nullable=False)
    vendor_id = Column(String, ForeignKey('vendor.id'), nullable=False)
    # TODO: add more fields
    vendor = relationship("VendorModel", back_populates="products")
    cpes = relationship("CPEModel", back_populates="product")

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the columns.
        """
        super().__init__(**kwargs)

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            # Get only the defined attributes from the class using __table__.columns
            attributes = {
                col.name: str(getattr(self, col.name)) for col in self.__table__.columns
                if getattr(self, col.name) is not None
            }

            # Create a string representation of the attributes sorted by key
            sorted_attributes_str = ''.join(f"{key}={value}" for key, value in sorted(attributes.items()))

            self.id = generate_id(sorted_attributes_str)
