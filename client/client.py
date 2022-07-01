import zmq, sys

if len(sys.argv) < 2:
    print("Usage: {} <server-ip-or-hostname>".format(sys.argv[0]))
    exit(1)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:50000".format(sys.argv[1]))

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending message PING (request {request}) …")
    socket.send(b"Ping")

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")