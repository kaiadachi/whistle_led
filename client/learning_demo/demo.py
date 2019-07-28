import tensorflow as tf
import model as model
import wave
import numpy as np
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE/10)
FILE_MODEL = "./model/model_4.ckpt"
RECORD_SECONDS = 1
DATA_LEN = RATE

print("=> init model")
model = model.Model((DATA_LEN))
model.load_model(FILE_MODEL)

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("録音を始めます。" + str(RECORD_SECONDS) + "秒間です")

frames = np.array([])
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    d = stream.read(CHUNK)
    d = np.frombuffer( d, dtype="int16") / 32768.0
    frames = np.append(frames, d)
print("録音を終了します")

fft = np.fft.fft(frames)
spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]
spectrum = np.array( spectrum, dtype=np.float32)
input_data = spectrum[np.newaxis,:]
output = model.get_sigout( input_data )

print("output:",output[0][0])

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
