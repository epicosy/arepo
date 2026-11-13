# arepo — examination database

Minimal PostgreSQL schema and seed data for the FindThemAll examination vertical slice.

## Run

Create the shared network once:

```sh
docker network create findthemall
```

Then build and run:

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

## Updating an existing local database container

Rebuild and recreate the container while retaining the named volume:

```sh
docker rm -f findthemall-db
docker build -t findthemall-arepo .
docker run -d --name findthemall-db --network findthemall -p 5432:5432 \
  -e POSTGRES_DB=findthemall -e POSTGRES_USER=findthemall \
  -e POSTGRES_PASSWORD=findthemall -v findthemall_pgdata:/var/lib/postgresql/data \
  findthemall-arepo
```

Do **not** remove `findthemall_pgdata`. The new entrypoint recognizes the existing `001` schema and applies any unapplied numbered migrations, including `002`, `003`, `004`, `005`, and `006`, to that volume.

## Model

An examination links independent root-cause and manifestation target threads. It is not a vulnerability record. Target, candidate-location, and reproduction source records are immutable inputs; reviewer decisions/notes live in separate review tables. Target and candidate records have `created_at` and `updated_at`; object locations are linked to manifestation targets and carry revision, source range, object name/type and CWE metadata. Annotations retain independent `kind` and `status` fields, carry a source `location_id`, and have `created_at`, `updated_at`, and submission metadata. Their `(model, model_id)` pair is polymorphic across candidate and object locations.

Migration `002_candidates_reproduction_unrar.sql` imports the candidate-location and reproduction records. Migration `003_root_cause_candidate_annotations.sql` corrects the UnRAR candidate revision to the root-cause target's `patch_base` revision (`637fc844…`), removes the second candidate whose revision does not exist in the project history, and imports two root-cause annotations. `004_target_timestamps_annotation_location.sql` adds target lifecycle timestamps and associates the root-cause annotations with location `07f838…`; it also seeds the operation annotation's rationale into its reviewer-note field. `005_manifestation_object_annotations.sql` creates the object-location relation for the final UnRAR chain weakness (`Dest[2]`, line 65) and imports its `resource.kind=buffer` and `resource.state=out-of-bounds` annotations. The chain README identifies its CWE label as CWE-787 (Out-of-bounds Write). `006_patch_reviews.sql` separates patch confirmation from the legacy target-definition review so an old target acceptance cannot incorrectly pre-approve patch analysis. The retained candidate keeps the correct patch-base function artifact ID. The original candidate file was stored under the crash-revision directory, but its `artifact_id` identifies the patch-base artifact; the migration resolves that inconsistency in favor of the target's explicit artifact association. The annotation `model_id` references the candidate-location ID, not the former bug ID.

## Artifact identity and integrity

Artifact IDs in the benchmark are SHA-256 digests of the exact stored artifact bytes. This prototype stores artifact text in PostgreSQL for local convenience, but does not yet verify the digest at import or read time. Before treating the database as authoritative, add an importer/constraint-side check that hashes the exact UTF-8 byte sequence (including line endings) and compares it with `artifact_id`. Do not normalize whitespace or line endings before hashing. The existing initial function-source seed is a local copy of the source snapshot; the integrity check is deliberately deferred, not waived.
