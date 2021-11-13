#!/usr/bin/env bash

for SQLFILE in /dumps/*.sql; do echo "Loading file: $SQLFILE\n" && psql -U $POSTGRES_USER "$POSTGRES_DB" < $SQLFILE; done
echo Done!
