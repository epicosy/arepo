from arepo.db import DatabaseConnection


def main():
    db_uri = "sqlite:///:memory:"
    print('Initializing the database.')
    engine = DatabaseConnection.init(db_uri)
    print('Database initialized.')
    print('engine:', engine)
    print('Getting database connection.')
    db = DatabaseConnection(db_uri, engine)
    print('Getting session.')
    session = db.get_session(scoped=True)
    from arepo.models.common.vulnerability import TagModel
    print('Querying tags.')
    tags = session.query(TagModel).all()

    for tag in tags:
        print(tag.id, tag.name)

    session.close()
    print('Session closed.')
    print('Done.')
