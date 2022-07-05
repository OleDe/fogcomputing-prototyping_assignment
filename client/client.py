import zmq, sys, json, time, threading
from gather_data import Gather_data
from db import cldb

def gather_data(db: cldb):
    gd = Gather_data()
    while 1:
        sleep(0.1)
        db.insert(gd.gather())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <server-ip-or-hostname>".format(sys.argv[0]))
        exit(1)

    context = zmq.Context()
    db = cldb()

    #  start inserting weather data to database
    data_thread = threading.Thread(target=gather_data, args=(db))
    data_thread.start()

    #  Socket to talk to server
    print("Connecting to server…")
    socket = context.socket(zmq.REP)
    socket.connect("tcp://{}:50000".format(sys.argv[1]))

    request = json.loads(socket.recv())
    while 1:
        data_to_send = db.get_data_latter_than(request['time'])
        for data in data_to_send:
            socket.send(json.dump(data))
            request = json.loads(socket.recv())

            if request['status'] == 'error':
                continue
    #  Do 10 requests, waiting each time for a response
    # for request in range(10):
    #     print(f"Sending message PING (request {request}) …")
    #     socket.send(b"Ping")

    #     #  Get the reply.
    #     message = socket.recv()
    #     print(f"Received reply {request} [ {message} ]")