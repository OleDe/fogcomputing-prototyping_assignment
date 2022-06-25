import socket, signal, os

conn = None
addr = None

def sig_handler(signum, frame):
    print("\nInterrupt by user")
    if conn:
        print("Close Connection...")
        conn.close()
    exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sig_handler)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Bind to 0.0.0.0:50000...")
    s.bind(('0.0.0.0', 50000))
    s.listen(1)
    while 1:
        print("Accepting...")
        conn, addr = s.accept()
        while 1:
            data = conn.recv(1024)
            print("recevied" + repr(data))
            if not data:
                break
            conn.sendall(data)
        conn.close()
