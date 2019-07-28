# for detection

import datetime
import os
import sys
import numpy as np
import pyaudio

import model as model

if len(sys.argv) == 2:
    RECORD_SECONDS = int(sys.argv[1])
else:
    RECORD_SECONDS = 30


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE/10)
project_dir = os.getcwd() + "/"

FILE_MODEL = "./model/model_4.ckpt"
DATA_LEN = RATE
print("=> init model")
model = model.Model((DATA_LEN))
model.load_model(FILE_MODEL)

def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frame = []
    all_whistle = []
    tmp = [False for k in range(20)]
    print("口笛の検出をします。検出時間は" + str(RECORD_SECONDS) + "秒間です")
    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        # convert data
        npData = np.frombuffer(data, dtype="int16") / 32768.0

        threshold = 0.06  # CAN BE CHANGED
        is_threshold_over = False
        if max(npData) > threshold:
            is_threshold_over = True

        tmp.append(is_threshold_over)
        tmp.pop(0)  # remove the oldest element

        frame.append(data)
        if len(frame) >= 20:
            frame.pop(0)

        # whistle detection
        # CAN BE IMPROVED!!
        if sum(tmp[7:13]) >= 3 and i >= 16:
            print("口笛検出")
            all_whistle.append(frame[5:15])
            tmp = [False for k in range(0, 20)]

            frm = frame[5:15]
            frames = np.array([])
            for f in frm:
                d = np.frombuffer(f, dtype="int16") / 32768.0
                frames = np.append(frames, d)
            fft = np.fft.fft(frames)
            spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
            spectrum = np.array(spectrum, dtype=np.float32)
            input_data = spectrum[np.newaxis, :]
            output = model.get_sigout(input_data)

            print("output:", output[0][0])

    stream.close()
    audio.terminate()
    print("検出終了")

if __name__ == "__main__":
    main()
