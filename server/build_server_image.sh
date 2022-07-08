#!/bin/sh

docker network create app-tier --driver bridge
docker run -d --name db-server \
    -e MONGO_INITDB_ROOT_USERNAME=serv \
    -e MONGO_INITDB_ROOT_PASSWORD=serv123 \
    -e MONGO_INITDB_DATABASE=serv_db \
    -p 27017:27017 \
    -v ./db:/data/db
    --network app-tier \
    --restart unless-stopped \
    mongo:4.4.6

docker build -f Dockerfile -t py-server:latest .
docker run -d --name py-server \
    -p 50000:50000 \
    --network app-tier \
    --restart unless-stopped \
    --entrypoint "python -u /server.py db-server 27017" \
    py-server:latest
