import socket
from contextlib import closing
import sys
import queue

def doSocket(queue):
    s = socket.socket()

    host = '172.20.10.5'
    port = 5000

    s.connect((host, port))

    try:
        while True:
            status = queue.get()
            print(status)
            if (status != "Error"):
                s.send(status.encode())

            print (host, s.recv(4096))
    except KeyboardInterrupt:
        print("close socket")
        s.close()

if __name__ == '__main__':
    doSocket(queue.Queue())
