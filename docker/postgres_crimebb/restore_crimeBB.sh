#!/usr/bin/env bash

for SQLFILE in /dumps/*.sql; do echo "Loading file: $SQLFILE\n" && psql -U $POSTGRES_USER "$POSTGRES_DB" < $SQLFILE; done
psql -U "$POSTGRES_USER" "$POSTGRES_DB" -c 'CREATE INDEX "index_Post_Site_Thread_Timestamp" ON public."Post" ("Site", "Thread", "Timestamp" ASC);'
psql -U "$POSTGRES_USER" "$POSTGRES_DB" -c 'CREATE INDEX "index_Post_Thread_Timestamp" ON public."Post" ("Thread", "Timestamp" ASC);'
psql -U "$POSTGRES_USER" "$POSTGRES_DB" -c 'CREATE INDEX "index_Thread_Forum" ON public."Thread" ("Forum");'
echo Done!
