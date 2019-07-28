# for detection
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
# import pprint
# pprint.pprint(sys.path)

import datetime
import numpy as np
import pyaudio

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
model = model_3class.Model((DATA_LEN, util.OUTPUT_SIZE))
model.load_model(FILE_MODEL)


def main(queue):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frame = []
    all_whistle = []
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
            output = model.get_softmax(input_data)
            max_index = np.argmax(output)
            print("output, class:", output, util.Status(max_index))
            queue.put(util.Status(max_index))
            is_detected = True

    stream.close()
    audio.terminate()
    print("検出終了")
    if(not is_detected):
        queue.put("Error")

if __name__ == "__main__":
    main()
