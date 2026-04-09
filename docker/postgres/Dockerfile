FROM postgres:14

COPY docker/postgres/create_databases.sh  /docker-entrypoint-initdb.d/create_databases.sh
RUN chmod +x /docker-entrypoint-initdb.d/create_databases.sh