import time, zmq, sys
from db import svdb

# TODO: Message validation

if len(sys.argv) < 3:
    print("Usage: {} <mongodb-ip-or-hostname> <db-port>".format(sys.argv[0]))
    exit(1)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50000")
print("Bound Zero Socket tcp://*:50000...")

print(f'connecting to db at {sys.argv[1]}:{sys.argv[2]}')
db = svdb(sys.argv[1], int(sys.argv[2]))

while True:
    #  Wait for message from client
    message = socket.recv_pyobj()
    print("Received request: {}".format(str(message)))

    # initial message
    stamp = db.get_latest_timestamp()
    if 'send_timestamp' in message:
        print('Sending latest timestamp: {}...'.format(stamp))
        response = {'time': stamp}

    # process consecutive messages
    else:
        if message['time'] <= stamp:
            print('deprecated data {} <= {}'.format(message['time'], stamp))
            response = {'time': stamp}
        else:
            db.insert({'air_pressure': message['air_pressure'], 'air_temperature': message['air_temperature'], 'time': message['time']})
            response = {'time': message['time']}
        
    # send request
    socket.send_pyobj(response)
