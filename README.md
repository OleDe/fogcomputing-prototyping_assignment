# prototyping_assignment
---

For the Fog Computing Summer Course at TU Berlin, we developed a simple distributed application. It consists of a Server and a Client that exchange weather data. The application is primarly implemented in Python and uses [ZeroMQ](https://zeromq.org/) library for messaging.

# Prerequisities
---

## Mandatory

`Docker` - the application is running in docker containers
`Python3`
`pymongo` - python library to query mongoDB databases
`pyzmq` - python zeroMQ messaging library

## Optional

`gcloud` - Google Cloud CLI (preferebly already initialized, see [link](https://cloud.google.com/sdk/docs/initializing))
`Docker-compose` - for running the multi-container application
`bmp280` - CLient is able to aquire data from a BMP280 temperature, pressure and altitude sensor

# Usage
---
Client and server containers can be deployed in the cloud and an edge node, or both on a single computer.
## Deploy Server
To build and start the server containers simply run `docker-compose -f server/docker-compose.yml up -d` in the parent directory and let docker compose do the work. This sets up two docker container, one for the server and one for the database that persistantly stores the data received from the client.
This can also be deployed in any VM. A Google Cloud VM with required firewall options, run `./scripts/build_gc.sh`.
## Deploy Client
To build and start the client containerson the edge node, pass the server ip accordingly when running docker compose `SERVER_HOSTNAME=<server-hostname-or-ip> docker-compose -f client/docker-compose.yml up -d`.
## Deploy on single node
The application can also be deployed on a single computer by running `docker-compose up -d` in the parent directory