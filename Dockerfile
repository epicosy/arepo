FROM postgres:17-alpine
ENV POSTGRES_DB=findthemall POSTGRES_USER=findthemall POSTGRES_PASSWORD=findthemall
COPY migrations/001_examination_unrar.sql /docker-entrypoint-initdb.d/001_examination_unrar.sql
