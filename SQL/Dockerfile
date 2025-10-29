FROM postgres:16

ENV POSTGRES_USER=git_user
ENV POSTGRES_PASSWORD=git_password
ENV POSTGRES_DB=git_database

COPY init.sql /docker-entrypoint-initdb.d/
