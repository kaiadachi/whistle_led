from enum import Enum
import pyaudio

class Status(Enum):
    RED = 0
    ON = 1
    OFF = 2
    NONE = 3

class Threshold:
    threshold1 = 0.15
    threshold2 = 0.05

class Data:
    def __init__(self, s, l):
        self.spectrum = s
        self.label = l

RED_DIR = "./training/red_data/"
ON_DIR = "./training/on_data/"
OFF_DIR = "./training/off_data/"
NONE_DIR = "./training/none_data/"

def get_dir(status):
    if status==Status.RED:
        return RED_DIR
    elif status==Status.ON:
        return ON_DIR
    elif status==Status.OFF:
        return OFF_DIR
    else:
        return NONE_DIR

PER_TRAIN = 0.95
CHUNK, RATE = 1024, 16000
DATA_LEN = RATE
OUTPUT_SIZE = len(Status)
FORMAT = pyaudio.paInt16
CHANNELS = 1

# for fft
AVERAGE =  2.2547496199583645
MAX =  178.20020581988499 / 2.0

# for mel
MEDIAN =  -35.069356381907625
MEL_DIV = 18

# for detection
start = int((CHUNK / 2 / 8) * 0.5)
end = int((CHUNK / 2 / 8) * 4)
