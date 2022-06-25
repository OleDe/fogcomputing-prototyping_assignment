import socket, sys

if __name__ == "__main__":
    gc_inst_ip = '34.159.196.33'
    if len(sys.argv) > 1:
        gc_inst_ip = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((gc_inst_ip, 50000))
    s.sendall('Hello, world')
    data = s.recv(1024)
    s.close()
    print 'Received', repr(data)
