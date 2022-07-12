import zmq, sys, time, threading
from gather_data import Gather_data
from db import cldb

# TODO: function comments, message validation

def gather_data(db: cldb):
    """
    continuously gather data from the sensor and store in the local database
    :param db: the database client
    """
    gd = Gather_data()
    while 1:
        time.sleep(0.1)
        db.insert(gd.gather())

class Client:
    def __init__(self, host, port='50000'):
        self.timeout = 5000
        self.host = host
        self.port = port
        self.addr = "tcp://{}:{}".format(self.host, self.port)
        self.context = zmq.Context()
        self.poller = zmq.Poller()
        self.socket = None
        self.reconnect()

    def reconnect(self):
        if self.socket:
            self.poller.unregister(self.socket)
            self.socket.disconnect(self.addr)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.linger = 0
        self.socket.setsockopt(zmq.REQ_CORRELATE, 1)
        self.socket.setsockopt(zmq.REQ_RELAXED, 1)
        self.socket.connect(self.addr)
        self.poller.register(self.socket, zmq.POLLIN)

    def recv(self):
        '''
        Receive data from server. Reconnect after timeout
        '''
        item = self.poller.poll(self.timeout)
        response = None
        if item:
            response = self.socket.recv_pyobj()
            print('received response: {}'.format(response))
        else:
            print("Server is not reachable. Reconnecting...")
            self.reconnect()
        return response
    
    def send(self, obj):
        '''
        Send Object to server
        '''
        print('Sending data: {}'.format(str(obj)))
        self.socket.send_pyobj(obj)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <server-ip-or-hostname> <mongodb-ip-or-hostname>".format(sys.argv[0]))
        exit(1)

    client = Client(sys.argv[1])
    client.reconnect()
    db = cldb(sys.argv[2])

    # start collecting data from sensor
    data_thread = threading.Thread(target=gather_data, args=(db,))
    data_thread.daemon = True
    data_thread.start()

    # make initial request
    response = None
    initial_request = {'send_timestamp': 1}
    request = initial_request

    while 1:
        # send data and receive timestamp
        while 1:
            client.send(request)
            response = client.recv()
            if response:
                print("erase data since {}...".format(response['time']))
                db.erase_data_starting_from(response['time'])
                break
            else:
                request = initial_request
        
        # aquire data from database 
        while 1:
            print('get data from db...')
            data = db.get_data_latter_than(response['time'])
            if data: 
                print("got {} from db...".format(data[0]))
                request = data[0]
                break
            print('No new data in database. Waiting...')
            time.sleep(0.2)
            