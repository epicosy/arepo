from arepo.base import Base
from arepo.mixins import EntityLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class VendorModel(Base, EntityLoaderMixin):
    __tablename__ = "vendor"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    # TODO: add more fields
    products = relationship("ProductModel", back_populates="vendor")

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the name.
        """
        super().__init__(**kwargs)
        assert self.name is not None, "URL must be provided."

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            self.id = generate_id(self.name)
