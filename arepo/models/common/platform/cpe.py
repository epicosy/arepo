from arepo.base import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship


class CPEModel(Base):
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


class CPEMatchModel(Base):
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
