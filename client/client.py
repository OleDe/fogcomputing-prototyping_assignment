import zmq, sys
from gather_data import Gather_data

if len(sys.argv) < 2:
    print("Usage: {} <server-ip-or-hostname>".format(sys.argv[0]))
    exit(1)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:50000".format(sys.argv[1]))

sensor = Gather_data(False)

#  Do 10 requests, waiting each time for a response
for request in range(10):

    # s
    data = sensor.gather()
    print(f"Sending weather data (request {request}): {data}")
    socket.send_json(data)

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")


