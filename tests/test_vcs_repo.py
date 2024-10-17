import pytest

from sqlalchemy.exc import IntegrityError

from arepo.models.source import SourceModel
from arepo.models.vcs.core.repository import RepositoryModel, RepositoryAssociationModel


# Repo data
repository_data = {
    'id': 'test-id',
    "name": 'tagify',
    "owner": 'yairEO',
    'available': True,
    'description': 'tags input component',
    'language': 'JavaScript',
    'size': 5410,
    'watchers': 20,
    'forks': 420,
    'stargazers': 3225
}


@pytest.mark.dependency(name="insert_repository")
def test_insert_repository(database_session):
    try:
        # Creating VulnerabilityModel object
        repository = RepositoryModel(
            id=repository_data['id'],
            name=repository_data['name'],
            owner=repository_data['owner'],
            available=repository_data['available'],
            description=repository_data['description'],
            language=repository_data['language'],
            size=repository_data['size'],
            watchers=repository_data['watchers'],
            forks=repository_data['forks'],
            stargazers=repository_data['stargazers']
        )

        # Inserting the object into the database
        database_session.add(repository)
        database_session.commit()

        source_id = database_session.query(SourceModel).filter_by(email="report@snyk.io").first().id

        # Creating RepositoryAssociationModel object
        repository_association = RepositoryAssociationModel(
            repository_id=repository_data['id'],
            vulnerability_id='CVE-2022-25854',
            source_id=source_id
        )

        # Inserting the object into the database
        database_session.add(repository_association)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting vulnerability")


@pytest.mark.dependency(depends=["insert_repository"])
def test_query_repository(database_session):
    # Querying the database for the object
    result = database_session.query(RepositoryModel).filter(RepositoryModel.id == repository_data['id']).first()

    # Asserting the result
    assert result.id == repository_data['id']
    assert result.name == repository_data['name']
    assert result.owner == repository_data['owner']
    assert result.available == repository_data['available']
    assert result.description == repository_data['description']
    assert result.language == repository_data['language']
    assert result.size == repository_data['size']
    assert result.watchers == repository_data['watchers']
    assert result.forks == repository_data['forks']
    assert result.stargazers == repository_data['stargazers']

    # Querying the database for the association object
    source_id = database_session.query(SourceModel).filter_by(email="report@snyk.io").first().id
    result = (database_session.query(RepositoryAssociationModel)
              .filter_by(repository_id=repository_data['id'])
              .filter_by(source_id=source_id)
              .filter_by(vulnerability_id='CVE-2022-25854')
              .first())

    # Asserting the result
    assert result is not None

