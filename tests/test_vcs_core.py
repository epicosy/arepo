import pytest
import dateutil.parser as date_parser

from arepo.models.vcs.core import RepositoryModel, CommitModel, CommitFileModel
from tests.test_vulnerability import vulnerability_data
from sqlalchemy.exc import IntegrityError


# Mocked vulnerability data
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


commit_data = {
    'id': 'test-commit-id',
    'sha': '198c0451fad188390390395ccfc84ab371def4c7',
    'url': 'https://api.github.com/repos/yairEO/tagify/commits/198c0451fad188390390395ccfc84ab371def4c7',
    'kind': 'patch',
    'date': date_parser.parse('2022-02-17T08:16:09Z'),
    'state': 'pending',
    'author': 'author',
    'message': 'fixes #989 - fix XSS',
    'changes': 2,
    'available': True,
    'additions': 1,
    'deletions': 1,
    'files_count': 1,
    'parents_count': 1,
    'repository_id': repository_data['id'],
    'vulnerability_id': vulnerability_data['cve']['id']
}


commit_file_data = {
    'id': 'test-commit-file-id',
    "filename": "src/tagify.js",
    "additions": 1,
    "deletions": 1,
    "changes": 2,
    "status": "modified",
    'extension': 'js',
    "patch": "@@ -101,7 +101,7 @@ Tagify.prototype = {\n \n         _s.disabled = input.hasAttribute('disabled')\n         _s.readonly = _s.readonly || input.hasAttribute('readonly')\n-        _s.placeholder = input.getAttribute('placeholder') || _s.placeholder || \"\"\n+        _s.placeholder = escapeHTML(input.getAttribute('placeholder') || _s.placeholder || \"\")\n         _s.required = input.hasAttribute('required')\n \n         for( let name in _s.classNames )",
    "raw_url": "https://github.com/yairEO/tagify/raw/198c0451fad188390390395ccfc84ab371def4c7/src%2Ftagify.js",
    'commit_id': commit_data['id']
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
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting vulnerability")


@pytest.mark.dependency(depends=["insert_repository"])
@pytest.mark.dependency(depends=["test_insert_vulnerability"])
@pytest.mark.dependency(name="test_insert_commit")
def test_insert_commit(database_session):
    try:
        # Creating VulnerabilityModel object
        commit = CommitModel(
            id=commit_data['id'],
            sha=commit_data['sha'],
            url=commit_data['url'],
            kind=commit_data['kind'],
            date=commit_data['date'],
            state=commit_data['state'],
            author=commit_data['author'],
            message=commit_data['message'],
            changes=commit_data['changes'],
            available=commit_data['available'],
            additions=commit_data['additions'],
            deletions=commit_data['deletions'],
            files_count=commit_data['files_count'],
            parents_count=commit_data['parents_count'],
            repository_id=commit_data['repository_id'],
            vulnerability_id=commit_data['vulnerability_id']
        )

        # Inserting the object into the database
        database_session.add(commit)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting vulnerability")


@pytest.mark.dependency(depends=["test_insert_commit"])
def test_insert_commit_file(database_session):
    try:
        # Creating VulnerabilityModel object
        commit_file = CommitFileModel(
            id=commit_file_data['id'],
            filename=commit_file_data['filename'],
            additions=commit_file_data['additions'],
            deletions=commit_file_data['deletions'],
            changes=commit_file_data['changes'],
            status=commit_file_data['status'],
            extension=commit_file_data['extension'],
            patch=commit_file_data['patch'],
            raw_url=commit_file_data['raw_url'],
            commit_id=commit_data['id']
        )

        # Inserting the object into the database
        database_session.add(commit_file)
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


@pytest.mark.dependency(depends=["test_insert_commit"])
def test_query_commit(database_session):
    result = database_session.query(CommitModel).filter(CommitModel.id == commit_data['id']).first()

    assert result.id == commit_data['id']
    assert result.sha == commit_data['sha']
    assert result.url == commit_data['url']
    assert result.kind == commit_data['kind']
    assert result.date.date() == commit_data['date'].date()
    assert result.state == commit_data['state']
    assert result.author == commit_data['author']
    assert result.message == commit_data['message']
    assert result.changes == commit_data['changes']
    assert result.available == commit_data['available']
    assert result.additions == commit_data['additions']
    assert result.deletions == commit_data['deletions']
    assert result.files_count == commit_data['files_count']
    assert result.parents_count == commit_data['parents_count']
    assert result.repository_id == commit_data['repository_id']
    assert result.vulnerability_id == commit_data['vulnerability_id']


@pytest.mark.dependency(depends=["test_insert_commit_file"])
def test_query_commit_file(database_session):
    result = database_session.query(CommitFileModel).filter(CommitFileModel.id == commit_file_data['id']).first()

    assert result.id == commit_file_data['id']
    assert result.filename == commit_file_data['filename']
    assert result.additions == commit_file_data['additions']
    assert result.deletions == commit_file_data['deletions']
    assert result.changes == commit_file_data['changes']
    assert result.status == commit_file_data['status']
    assert result.extension == commit_file_data['extension']
    assert result.patch == commit_file_data['patch']
    assert result.raw_url == commit_file_data['raw_url']
    assert result.commit_id == commit_data['id']
