import socket
from datetime import datetime
from time import sleep
from raspi_controller import *

def recieveSocket(host='172.20.10.5', port=5000):
    s = socket.socket()
    s.bind((host, port))
    setup()

    try:
        print 'listening'
        s.listen(5)
        c, addr = s.accept()

        flg = True
        while flg:
            print 'receiving'
            recieve = c.recv(4096).decode()
            print recieve

            print 'sending'
            c.send("from server: " + recieve)

            if(recieve == '0'):
                connectRed()
            elif(recieve == '1'):
                connectAll()
            elif(recieve == '2'):
                disconnect()
            elif(recieve == 'fin'):
                flg = False
                c.close()
            else:
                pass
        s.close()

    except Exception as e:
        print e
        c.close()
        s.close()


if __name__ == '__main__':
    recieveSocket()
