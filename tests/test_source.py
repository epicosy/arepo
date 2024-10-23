import pytest

from arepo.models.source import SourceModel

source_data = [
    {
        "id": "snyk-source",
        "name": "Snyk",
        "email": "report@snyk.io"
    },
    {
        "id": "nvd-source",
        "name": "NVD",
        "email": "nvd@nist.gov"
    }
]


@pytest.mark.dependency(name="test_insert_sources")
def test_insert_sources(database_session):
    from sqlalchemy.exc import IntegrityError
    for source in source_data:
        try:
            source_model = SourceModel(
                id=source["id"],
                name=source["name"],
                email=source["email"]
            )
            database_session.add(source_model)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()
            pytest.fail("IntegrityError occurred while inserting source")


@pytest.mark.dependency(depends=["test_insert_sources"])
def test_get_inserted_sources(database_session):
    # Query the database to retrieve the inserted sources
    retrieved_sources = database_session.query(SourceModel).all()

    # Check if the retrieved sources exist
    assert len(retrieved_sources) == len(source_data)

    for source in retrieved_sources:
        assert source.name in [s["name"] for s in source_data]
        assert source.email in [s["email"] for s in source_data]
