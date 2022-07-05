import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind("tcp://*:50000")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    print("Replying Pong...")
    socket.send(b"Pong")