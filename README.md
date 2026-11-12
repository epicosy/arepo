# arepo — examination database

Minimal PostgreSQL schema and seed data for the FindThemAll examination vertical slice.

## Run

```sh
docker build -t findthemall-arepo .
docker run -d --name findthemall-db --network findthemall -p 5432:5432 \
  -e POSTGRES_DB=findthemall -e POSTGRES_USER=findthemall \
  -e POSTGRES_PASSWORD=findthemall -v findthemall_pgdata:/var/lib/postgresql/data \
  findthemall-arepo
```

The image applies numbered migrations on every container startup, recording completed files in `schema_migrations`. This also applies newly added migrations to an existing persistent volume; the initial `001` schema is baselined when its tables already exist. To inspect migration state:

```sh
docker exec findthemall-db psql -U findthemall -d findthemall -c "TABLE schema_migrations"
```

Credentials above are for local development only.

## Model

An examination links independent root-cause and manifestation target threads. It is not a vulnerability record. Target, candidate-location, and reproduction source records are immutable inputs; reviewer decisions/notes live in separate review tables.

Migration `002_candidates_reproduction_unrar.sql` imports the two candidate-location records and one reproduction record for UnRAR, including its runner log and execution context. Candidate revision IDs are retained from their storage paths. The source corpus currently has a discrepancy worth reviewing: both candidate JSON records point to the root-cause target, although the candidate migration guidance describes the crash-side candidate as belonging to the manifestation target. This seed preserves the source records as stored rather than silently changing their relationships.

## Artifact identity and integrity

Artifact IDs in the benchmark are SHA-256 digests of the exact stored artifact bytes. This prototype stores artifact text in PostgreSQL for local convenience, but does not yet verify the digest at import or read time. Before treating the database as authoritative, add an importer/constraint-side check that hashes the exact UTF-8 byte sequence (including line endings) and compares it with `artifact_id`. Do not normalize whitespace or line endings before hashing. The existing initial function-source seed is a local copy of the source snapshot; the integrity check is deliberately deferred, not waived.
