# TFM - Sale of access IoT devices in underground forums


## About

This repository is part of final work for [Data Science master's degree at UOC (Universitat Oberta de Calatunya)](!https://estudios.uoc.edu/es/masters-universitarios/data-science/presentacion).

The aim of this project is to explore and analyze the sale of access IoT devices in underground forums.

## Requirements

- Git.
- Docker and Docker-compose.
- Source SQL data files (not provided in this repository).

## Project setup

Clone repository

```
git clone git@github.com:serfer2/tfm.git
cd tfm

```

Create `.env` vars file for PostgresDB:

```
cp docker/postgres_crimebb/local.env docker/postgres_crimebb/.env
```

Remember to set variable values with desired user and password. Do not change `POSTGRES_DB` value!

Build and run containers:

```
docker-compose up -d
```

Hydrate DB with SQL dump files:

```
sudo docker-compose exec crimebb sh "/usr/local/bin/restore.sh"
```

Now, Postgres project database is up and accesible in `localhost` port `5432`.

DB connection credentials are the same you've set in `docker/postgres_crimebb/.env` file.

**NOTE**

You'll need to place `.sql` dump files in folder `../called dumps_crimebb` (one level hihger than current dir)

## TIPS

Postgres DB data is stored inside project folder, in `postgres-data` directory.

There's no need to run DB hydratation more than once.

In the case you get some permission errors when trying to run project containers, all you have to do is to get permissions for Postgres DB data directory before running containers:

```
sudo chown -R $USER postgres-data && docker-compose up -d
```

## Author

Sergio Fernández García serfer2@protonmail.com