# prototyping_assignment

## What it does

The "client" (client/client.py) runs on an edge device and continuously collects weather data (temparature, air pressure)
using a sensor. These weather data are then sent to the "server" (server/server.py) running on a cloud node. The server
persistently stores the weather data in a database which is also located on the same cloud node.

To prevent the loss of data in case the server crashes or the connection between the cloud and the edge is interrupted,
there is also a database instance on the edge device. When the client cannot reach the server, it temporarily stores
the data in this local database instance until the connection is re-established. Then, the client fetches all the data
yet unknown to the server from its database, deletes the respective database entries, and forwards the data to the server.

## How it works

## How to use the application

### Local-Only

To use the application locally, use the docker-compose.yml script at the root of the project, i.e. run:
```
docker compose up --build -d
```

This will start four docker containers: one for the server (py-server), one for the client (py-client), and two for the
database instances.

### Distributed Environment