# Homework 1 Solution

## Q1

```bash
docker run -it --rm --platform=linux/amd64 --entrypoint /bin/bash python:3.12.8
```

in docker container run

```bash
pip --version
```

```plaintext
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

## Q2

Jippydy said:

The correct hostname and port for pgAdmin to connect to the Postgres database in the given docker-compose.yaml are:

> db:5432

<!--
Explanation:
1.	Hostname:
    - Within a Docker Compose network, services can communicate using their service names as hostnames.
	-	The db service name can be used as the hostname to connect to the Postgres database.
2.	Port:
	-	Inside the Docker Compose network, containers communicate using the container’s internal ports.
	-	The db service exposes Postgres on its internal port 5432 (the standard Postgres port). The external mapping 5433:5432 is irrelevant for communication between services in the same network.

Why Not the Others?
-	postgres:5433: The container name (postgres) cannot be used as a hostname, and 5433 is the port mapped to the host, not within the Docker network.
-	localhost:5432: localhost refers to the host machine, not the Docker network.
-	postgres:5432: The correct service name is db, not postgres.
-	db:5433: Inside the Docker network, Postgres listens on its internal port 5432, not 5433.
The correct hostname and port for pgAdmin to connect to the Postgres database in the given docker-compose.yaml are:

db:5432

Explanation:
1. Hostname:
   - Within a Docker Compose network, services can communicate using their service names as hostnames.
   - The db service name can be used as the hostname to connect to the Postgres database.
2. Port:
   - Inside the Docker Compose network, containers communicate using the container’s internal ports.
   - The db service exposes Postgres on its internal port 5432 (the standard Postgres port). The external mapping 5433:5432 is irrelevant for communication between services in the same network.

Why Not the Others?
- postgres:5433: The container name (postgres) cannot be used as a hostname, and 5433 is the port mapped to the host, not within the Docker network.
- localhost:5432: localhost refers to the host machine, not the Docker network.
- postgres:5432: The correct service name is db, not postgres.
- db:5433: Inside the Docker network, Postgres listens on its internal port 5432, not 5433. -->

## 