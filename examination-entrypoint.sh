#!/usr/bin/env bash
set -Eeuo pipefail

# Start the official PostgreSQL entrypoint in the background. It initializes a
# new data directory and then starts the server; existing volumes are reused.
docker-entrypoint.sh postgres &
postgres_pid=$!

shutdown() {
  kill -TERM "$postgres_pid" 2>/dev/null || true
  wait "$postgres_pid" 2>/dev/null || true
}
trap shutdown TERM INT

db_ready=0
for _ in $(seq 1 60); do
  if pg_isready -h 127.0.0.1 -p 5432 -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-postgres}" >/dev/null 2>&1; then
    db_ready=1
    break
  fi
  if ! kill -0 "$postgres_pid" 2>/dev/null; then
    wait "$postgres_pid"
    exit $?
  fi
  sleep 1
done

if [ "$db_ready" -ne 1 ]; then
  echo "PostgreSQL did not become ready within 60 seconds" >&2
  exit 1
fi

psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -v ON_ERROR_STOP=1 <<'SQL'
CREATE TABLE IF NOT EXISTS schema_migrations (
  version text PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT now()
);
SQL

# Existing installations were initialized with migration 001 through the
# upstream image's init directory. Mark that baseline before applying 002.
has_examinations=$(psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -Atqc "SELECT to_regclass('public.examinations') IS NOT NULL")
if [ "$has_examinations" = "t" ]; then
  psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -v ON_ERROR_STOP=1 -c "INSERT INTO schema_migrations(version) VALUES ('001_examination_unrar.sql') ON CONFLICT DO NOTHING"
fi

for migration in /migrations/[0-9]*.sql; do
  [ -f "$migration" ] || continue
  version=$(basename "$migration")
  applied=$(psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -Atqc "SELECT 1 FROM schema_migrations WHERE version = '$version'")
  if [ "$applied" != "1" ]; then
    echo "Applying migration $version"
    psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -v ON_ERROR_STOP=1 -f "$migration"
    psql --username "${POSTGRES_USER:-postgres}" --dbname "${POSTGRES_DB:-postgres}" -v ON_ERROR_STOP=1 -c "INSERT INTO schema_migrations(version) VALUES ('$version')"
  fi
done

wait "$postgres_pid"
