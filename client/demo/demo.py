# for detection
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
# import pprint
# pprint.pprint(sys.path)

import datetime
import numpy as np
import pyaudio
import queue
import librosa
from common import model_3class, util

if len(sys.argv) == 2:
    RECORD_SECONDS = int(sys.argv[1])
else:
    RECORD_SECONDS = 30


FORMAT = util.FORMAT
CHANNELS = util.CHANNELS
RATE = util.RATE
CHUNK = int(RATE/10)
FILE_MODEL = "./model/model_3class.ckpt"
DATA_LEN = RATE

print("=> init model")
model = model_3class.Model((2048, util.OUTPUT_SIZE))
model.load_model(FILE_MODEL)


def main():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frame = []
    tmp = [False for k in range(20)]
    is_detected = False
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
            frm = frame[5:15]
            frames = np.array([])
            for f in frm:
                d = np.frombuffer(f, dtype="int16") / 32768.0
                frames = np.append(frames, d)


            S = librosa.feature.melspectrogram(y=frames, sr=util.RATE, n_mels=128, hop_length=1024)
            log_S = librosa.power_to_db(S)
            ret = (log_S.reshape(-1) - util.MEDIAN) / util.MEL_DIV
            input_data = ret[np.newaxis, :]

            # fft = np.fft.fft(frames)
            # spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
            # spectrum = np.array(spectrum, dtype=np.float32)
            # input_data = spectrum[np.newaxis, :]
            
            output = model.get_softmax(input_data)
            max_index = np.argmax(output)
            print("output, class:", output, util.Status(max_index))
            tmp = [False for k in range(20)]


    stream.close()
    audio.terminate()
    print("検出終了")

if __name__ == "__main__":
    main()
    
