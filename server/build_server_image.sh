#!/bin/sh

docker build -f Dockerfile -t server:latest .
docker run -p 50000:50000 server:latest