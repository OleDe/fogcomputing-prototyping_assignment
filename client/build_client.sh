#!/bin/bash

docker network create client-mongodb --driver bridge
docker run -d --name client-mongodb-server \
    -e MONGO_INITDB_ROOT_USERNAME=cl \
    -e MONGO_INITDB_ROOT_PASSWORD=cl123 \
    -e MONGO_INITDB_DATABASE=cl_db \
    -p 27017:27017 \
    --network client-mongodb \
    mongo:4.4.6

# docker build -f Dockerfile -t client:latest .
# docker run -d --name client\
#     --network client-mongodb \
#     client:latest