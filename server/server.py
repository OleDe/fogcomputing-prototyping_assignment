import time
import zmq

from db import cldb

context = zmq.Context()
socket = context.socket(zmq.REP)

print('listening on 0.0.0.0:50000')
socket.bind("tcp://*:50000")

db_client = cldb()
print('connected to mongo db instance')

while True:
    #  Wait for next request from client
    timestamp, air_temp, air_pressure = tuple(socket.recv_json())
    print(f"Received request: {timestamp, air_temp, air_pressure}")

    db_client.insert(air_pressure, air_temp, timestamp)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"Processed")
