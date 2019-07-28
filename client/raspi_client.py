import socket
from contextlib import closing
import sys

def doSocket(output):
    s = socket.socket()

    host = '172.20.10.5'
    port = 5000

    s.connect((host, port))

    if(output >= 0.5):
        s.send(b"1")
    else:
        s.send(b"0")

    print (host, s.recv(4096))

    s.close()

if __name__ == '__main__'
    doSocket(0.8)
