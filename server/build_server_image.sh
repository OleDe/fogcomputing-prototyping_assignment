#!/bin/sh

docker network create server-mongodb --driver bridge
docker run -d --name server-mongodb-server \
    -e MONGO_INITDB_ROOT_USERNAME=serv \
    -e MONGO_INITDB_ROOT_PASSWORD=serv123 \
    -e MONGO_INITDB_DATABASE=serv_db \
    -p 27018:27017 \
    --network server-mongodb \
    mongo:4.4.6

# docker build -f Dockerfile -t server:latest .
# docker run -d -p 50000:50000 server:latest
