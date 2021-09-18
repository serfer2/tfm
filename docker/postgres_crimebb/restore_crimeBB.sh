#!/usr/bin/env bash

# psql -c 'CREATE DATABASE $POSTGRES_DB'
# psql -c 'ALTER DATABASE POSTGRES_DB OWNER TO POSTGRES_USER'
for SQLFILE in /dumps/*.sql; do echo "Loading file: $SQLFILE\n" && psql "$POSTGRES_DB" < $SQLFILE; done
echo Done!
