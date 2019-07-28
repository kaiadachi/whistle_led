import threading
import queue
from raspi_client import *
from demo.simple_detection import *

if __name__ == "__main__":
    queue = queue.Queue()
    socket = threading.Thread(target=doSocket, args=(queue,))
    detection = threading.Thread(target=main, args=(queue,))
    socket.start()
    detection.start()