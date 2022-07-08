# prototyping_assignment
---
## What it does

The "client" (client/client.py) runs on an edge device and continuously collects weather data (temparature, air pressure)
using a sensor. These weather data are then sent to the "server" (server/server.py) running on a cloud node. The server
persistently stores the weather data in a database which is also located on the same cloud node.

To prevent the loss of data in case the server crashes or the connection between the cloud and the edge is interrupted,
there is also a database instance on the edge device. When the client cannot reach the server, it temporarily stores
the data in this local database instance until the connection is re-established. Then, the client fetches all the data
yet unknown to the server from its database, deletes the respective database entries, and forwards the data to the server.

## How it works
## Prerequisities

Mandatory:

 - `Docker` - the application is running in docker containers
 - `Python3`
 - `pymongo` - python library to query mongoDB databases
 - `pyzmq` - python zeroMQ messaging library

Optional:

 - `gcloud` - Google Cloud CLI (preferebly already initialized, see [link](https://cloud.google.com/sdk/docs/initializing))
 - `Docker-compose` - for running the multi-container application
 - `bmp280` - CLient is able to aquire data from a BMP280 temperature, pressure and altitude sensor
## How to use the application
Client and server containers can be deployed in the cloud and an edge node, or both on a single computer.

### Deploy Server
To build and start the server simply run 
```
docker-compose -f server/docker-compose.yml up -d
```
in the parent directory and let docker compose do the work. This sets up two docker containers, one for the server and one for the database that persistantly stores the data received from the client.


Alternatively, this can also be deployed in any VM. To host a Google Cloud VM, run:
```
./scripts/build_gc.sh
```
This creates a container-optimized OS, exports a ssh-key as project metadata and prints the servers external ip. Now log in via SSH, download the repository and execute the build script:
```
ssh -i id_rsa foggy@<server-ip>
git clone <path-to-this-rep>
cat <rep-name>/server/build_server_image.sh | sh
```

### Deploy Client
To build and start the client on the edge node, pass the server ip accordingly when running docker compose:
```
SERVER_HOSTNAME=<server-ip> docker-compose -f client/docker-compose.yml up -d
```

### Local-Only

To use the application locally, use the docker-compose.yml script at the root of the project, i.e. run:
```
docker compose up --build -d
```

This will start four docker containers: one for the server (py-server), one for the client (py-client), and two for the
database instances.
