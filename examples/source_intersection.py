from os import environ
from arepo.db import DatabaseConnection
from arepo.models.vcs.core.repository import RepositoryAssociationModel
from arepo.models.vcs.core.commit import CommitAssociationModel

from sqlalchemy.orm import aliased


def get_overlap_vulnerability_ids(session, model, join_column, source_1, source_2):
    # Create aliases for the model
    alias_1 = aliased(model)
    alias_2 = aliased(model)

    # Perform the query
    return session.query(
        alias_1.vulnerability_id
    ).distinct().join(
        alias_2,
        (alias_1.vulnerability_id == alias_2.vulnerability_id)
    ).filter(
        alias_1.source_id == source_1,
        alias_2.source_id == source_2
    ).all()


db = DatabaseConnection(environ['SQLALCHEMY_DATABASE_URI'])
session = db.get_session(scoped=True)


print("CVEs with repositories in NVD and OSV",
      len(
          get_overlap_vulnerability_ids(
              session,
              model=RepositoryAssociationModel,
              join_column='repository_id',
              source_1='nvd_id',
              source_2='osv_id'
          )
      )
)

print("CVEs with commits in NVD and OSV",
      len(
          get_overlap_vulnerability_ids(
              session,
              model=CommitAssociationModel,
              join_column='commit_id',
              source_1='nvd_id',
              source_2='osv_id'
          )
      )
)

session.close()
