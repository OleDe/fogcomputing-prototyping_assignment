import time, zmq
from db import svdb

# TODO: Message validation

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:50000")
print("Bound Zero Socket tcp://*:50000...")

db = svdb()

while True:
    #  Wait for next request from client
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
        
    # send response
    socket.send_pyobj(response)
