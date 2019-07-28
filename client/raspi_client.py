import socket
from contextlib import closing
import sys
import queue
import traceback

def doSocket(queue):
    s = socket.socket()

    host = '172.20.10.5'
    port = 5000

    s.connect((host, port))

    try:
        while True:
            status = queue.get()
            print("catch" + status)
            if (status != "fin"):
                s.send(status.encode())
            else:
                s.send(status.encode())
                break

            print (s.recv(4096))

    except KeyboardInterrupt:
        traceback.print_exc()
        print("except!!")
        print("close socket")
        s.close()

    print("close socket")
    s.close()

if __name__ == '__main__':
    doSocket(queue.Queue())