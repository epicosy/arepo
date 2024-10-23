from arepo.base import Base
from arepo.mixins import EntityLoaderMixin
from arepo.utils.misc import generate_id

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class CPEModel(Base, EntityLoaderMixin):
    __tablename__ = "cpe"

    id = Column('id', String, primary_key=True)
    product_id = Column(String, ForeignKey('product.id'), nullable=False)
    version = Column(String, nullable=True, default="*")
    update = Column(String, nullable=True, default="*")
    edition = Column(String, nullable=True, default="*")
    language = Column(String, nullable=True, default="*")
    sw_edition = Column(String, nullable=True, default="*")
    target_sw = Column(String, nullable=True, default="*")
    target_hw = Column(String, nullable=True, default="*")
    other = Column(String, nullable=True, default="*")

    product = relationship("ProductModel", back_populates="cpes")
    cpe_matches = relationship("CPEMatchModel", back_populates="cpe")

    def __init__(self, **kwargs):
        """
            If the ID is not provided, it will be generated from the columns.
        """
        super().__init__(**kwargs)

        if self.id is None:
            # TODO: should be defined as read-only in the schema to avoid issues with future changes
            # Get only the defined attributes from the class using __table__.columns
            attributes = {}

            for col in self.__table__.columns:
                if col.name == 'id':
                    continue

                if getattr(self, col.name) is None:
                    # Set the default value, to ensure consistency
                    attributes[col.name] = col.default.arg
                else:
                    attributes[col.name] = str(getattr(self, col.name))

            # Create a string representation of the attributes sorted by key
            sorted_attributes_str = ''.join(f"{key}={value}" for key, value in sorted(attributes.items()))

            self.id = generate_id(sorted_attributes_str)


class CPEMatchModel(Base, EntityLoaderMixin):
    __tablename__ = "cpe_match"

    id = Column('id', String, primary_key=True)
    cpe_id = Column(String, ForeignKey('cpe.id'), nullable=False)
    node_id = Column(String, ForeignKey('node.id'), nullable=False)
    vulnerable = Column(Boolean, nullable=False)
    version_start_including = Column(String, nullable=True)
    version_start_excluding = Column(String, nullable=True)
    version_end_including = Column(String, nullable=True)
    version_end_excluding = Column(String, nullable=True)

    cpe = relationship("CPEModel", back_populates="cpe_matches")
    node = relationship("NodeModel", back_populates="cpe_matches")
