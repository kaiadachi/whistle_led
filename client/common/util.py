from enum import Enum
import pyaudio

class Status(Enum):
    RED = 0
    ON = 1
    OFF = 2

class Data:
    def __init__(self, s, l):
        self.spectrum = s
        self.label = l

RED_DIR = "./training/red_data/"
ON_DIR = "./training/on_data/"
OFF_DIR = "./training/off_data/"

NUM_EPOCH , NUM_BATCH = 2, 32
PER_TRAIN = 0.9
CHUNK, RATE = 1024, 16000
DATA_LEN = RATE
OUTPUT_SIZE = 3
FORMAT = pyaudio.paInt16
CHANNELS = 1

AVERAGE =  2.2547496199583645
MAX =  178.20020581988499 / 2.0
