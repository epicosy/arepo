import pytest

from arepo.models.vcs.diff import DiffBlockModel, ChangeModel


diff_data = {
    'diff_blocks': [
        {
            'id': 'test-diff-block-id',
            'order': 2,
            'a_path': 'src/tagify.js',
            'changes': [
                {
                    'id': 'test-change-id-1',
                    'line': 104,
                    'start_col': 9,
                    'end_col': 82,
                    'type': 'deletion',
                    'content': '        _s.placeholder = input.getAttribute(\'placeholder\') || _s.placeholder || ""'
                },
                {
                    'id': 'test-change-id-2',
                    'line': 104,
                    'start_col': 9,
                    'end_col': 94,
                    'type': 'addition',
                    'content': '        _s.placeholder = escapeHTML(input.getAttribute(\'placeholder\') || _s.placeholder || "")',
                }
            ],
            'commit_file_id': 'test-commit-file-id'
        }
    ]
}


@pytest.mark.dependency(name="insert_diff_block")
def test_insert_diff_block(database_session):
    from sqlalchemy.exc import IntegrityError

    try:
        diff_block = DiffBlockModel(
            id=diff_data['diff_blocks'][0]['id'],
            order=diff_data['diff_blocks'][0]['order'],
            a_path=diff_data['diff_blocks'][0]['a_path'],
            commit_file_id=diff_data['diff_blocks'][0]['commit_file_id']
        )

        database_session.add(diff_block)
        database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting diff block")


@pytest.mark.dependency(depends=["insert_diff_block"])
@pytest.mark.dependency(name="insert_changes")
def test_insert_changes(database_session):
    from sqlalchemy.exc import IntegrityError

    try:
        for change_data in diff_data['diff_blocks'][0]['changes']:
            change = ChangeModel(
                id=change_data['id'],
                line=change_data['line'],
                start_col=change_data['start_col'],
                end_col=change_data['end_col'],
                type=change_data['type'],
                content=change_data['content'],
                diff_block_id=diff_data['diff_blocks'][0]['id']
            )

            database_session.add(change)
            database_session.commit()
    except IntegrityError:
        database_session.rollback()
        pytest.fail("IntegrityError occurred while inserting changes")

