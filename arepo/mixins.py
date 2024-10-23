from sqlalchemy.inspection import inspect


class EntityLoaderMixin:
    """Mixin to handle session-based loading operations for regular models."""

    @classmethod
    def get_all_ids(cls, session):
        return set(id_tuple[0] for id_tuple in session.query(cls.id).all())

    @classmethod
    def load_all(cls, session):
        return session.query(cls).all()


class AssociationLoaderMixin:
    """Mixin to handle session-based loading operations for association models."""

    @property
    def composite_id(self):
        """Generate a composite ID based on the primary key fields."""
        mapper = inspect(self.__class__)  # Get the mapper for the class, not the instance
        primary_key_values = [getattr(self, key.name) for key in mapper.primary_key]
        return "_".join(str(value) for value in primary_key_values)

    @classmethod
    def get_all_ids(cls, session):
        """Generate composite keys for association models using primary key fields."""
        primary_keys = [key.name for key in inspect(cls).primary_key]

        # Query all the rows in the association table
        rows = session.query(cls).all()

        # Create a set of composite keys based on the primary key fields
        composite_keys = set(
            "_".join(str(getattr(row, key)) for key in primary_keys)
            for row in rows
        )

        return composite_keys
