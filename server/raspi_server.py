import socket
from datetime import datetime
from time import sleep
from raspi_controller import *

def recieveSocket(host='172.20.10.5', port=5000):
    s = socket.socket()
    s.bind((host, port))

    flg = True
    while flg:
        print 'listening'
        s.listen(5)
        c, addr = s.accept()
        print 'receiving'
        recieve = c.recv(4096)
        print recieve
        print 'sending'
        c.send(recieve)
        if(recieve == b'1'):
        	run()
            flg = False
            c.close()
    s.close()

if __name__ == '__main__':
    recieveSocket()
