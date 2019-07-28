import datetime
import os
import sys
import wave
import pyaudio

if len(sys.argv) == 2:
    RECORD_SECONDS = int(sys.argv[1])
else:
    RECORD_SECONDS = 100

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE/10)

project_dir = os.getcwd() + "/training/"

audio = pyaudio.PyAudio()

if not os.path.exists(project_dir + "noise_data"):
    os.mkdir(project_dir + "noise_data")

frame_dict = {}
for t in range(RECORD_SECONDS):
    frames = []
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print(t+1, " record")
    for i in range(int(RATE / CHUNK * 1)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.close()
    stream.stop_stream()
    now = datetime.datetime.now()
    file_name = project_dir + "noise_data/" + "noise_{0:%Y%m%d%H%M%S.%s}.wav".format(now)
    frame_dict[file_name] = frames
    # print(file_name)
    print("end")


audio.terminate()
for k, v in frame_dict.items():
    waveFile = wave.open(k, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(v))
    waveFile.close()