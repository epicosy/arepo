from os import environ
from arepo.db import DatabaseConnection
from arepo.models.vcs.core.repository import RepositoryAssociationModel
from arepo.models.vcs.core.commit import CommitAssociationModel

from sqlalchemy import func
from sqlalchemy.orm import aliased


def get_non_overlap_vulnerability_ids(session, model, source_1, source_2):
    alias_1 = aliased(model)
    alias_2 = aliased(model)

    # Query to find vulnerabilities in source_1 but not in source_2
    return session.query(
        alias_1.vulnerability_id
    ).distinct().outerjoin(
        alias_2,
        (alias_1.vulnerability_id == alias_2.vulnerability_id) &
        (alias_2.source_id == source_2)
    ).filter(
        alias_1.source_id == source_1,
        alias_2.vulnerability_id == None  # Where there's no match in source_2
    ).all()


db = DatabaseConnection(environ['SQLALCHEMY_DATABASE_URI'])
session = db.get_session(scoped=True)

print(
    "Total CVEs with repositories:",
    session.query(RepositoryAssociationModel.vulnerability_id).distinct().count()
)

print(
    "Total CVEs with commits:",
    session.query(CommitAssociationModel.vulnerability_id).distinct().count()
)

print("Repository Duplicates:",
      len(session.query(RepositoryAssociationModel.vulnerability_id).
          group_by(RepositoryAssociationModel.vulnerability_id).
          having(func.count(RepositoryAssociationModel.repository_id) > 1).
          all()
          )
      )

print("Commit Duplicates:",
      len(session.query(CommitAssociationModel.vulnerability_id).
          group_by(CommitAssociationModel.vulnerability_id).
          having(func.count(CommitAssociationModel.commit_id) > 1).
          all()
          )
      )


print("CVEs with repositories in NVD and not in OSV:",
      len(
          get_non_overlap_vulnerability_ids(
              session,
              model=RepositoryAssociationModel,
              source_1='nvd_id',
              source_2='osv_id'
          )
      )
      )

print("CVEs with repositories in OSV and not in NVD:",
      len(
          get_non_overlap_vulnerability_ids(
              session,
              model=RepositoryAssociationModel,
              source_1='osv_id',
              source_2='nvd_id'
          )
      )
      )

print("CVEs with commits in NVD and not in OSV:",
      len(
          get_non_overlap_vulnerability_ids(
              session,
              model=CommitAssociationModel,
              source_1='nvd_id',
              source_2='osv_id'
          )
      )
      )

print("CVEs with commits in OSV and not in NVD:",
      len(
          get_non_overlap_vulnerability_ids(
              session,
              model=CommitAssociationModel,
              source_1='osv_id',
              source_2='nvd_id'
          )
      )
      )

session.close()
