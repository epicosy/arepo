from arepo.base import Base

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class SourceModel(Base):
    __tablename__ = "source"

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False)

    # Relationship to ReferenceAssociationModel
    references = relationship(
        'ReferenceAssociationModel',
        back_populates='source'
    )

    tags = relationship(
        'TagAssociationModel',
        back_populates='source'
    )
