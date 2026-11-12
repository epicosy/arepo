# arepo — examination database

Minimal PostgreSQL schema for the FindThemAll examination vertical slice.

## Run

```sh
docker build -t findthemall-arepo .
docker run -d --name findthemall-db -p 5432:5432 -e POSTGRES_DB=findthemall -e POSTGRES_USER=findthemall -e POSTGRES_PASSWORD=findthemall -v findthemall_pgdata:/var/lib/postgresql/data findthemall-arepo
```

The official PostgreSQL image applies SQL files in `/docker-entrypoint-initdb.d` on first initialization of an empty data directory. Remove the container and volume to reset. Credentials are local-development only.

An examination links independent root-cause and manifestation target threads. It is not a vulnerability record. Target input is immutable; reviewer state is stored separately.
