import datetime
import os
import sys
import wave
import pyaudio
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
from common import util
# import matplotlib.pyplot as plt

if len(sys.argv) == 2:
    RECORD_NUMBER = int(sys.argv[1])
else:
    RECORD_NUMBER = 10


RECORD_SECONDS = 100
FORMAT = util.FORMAT
CHANNELS = util.CHANNELS
RATE = util.RATE
CHUNK = int(RATE/10)
project_dir = os.getcwd() + "/training/"


def main():
    frames = []
    all_whistle = {}
    tmp = [False for k in range(20)]
    audio = pyaudio.PyAudio()
    is_data_exist = [False for k in range(3)]

    start = util.start
    end = util.end
    # axis_x = np.fft.fftfreq(CHUNK, d=1.0 / RATE)

    print("口笛の検出をします。検出回数は" + str(RECORD_NUMBER) + "、各検出の秒数は" + str(RECORD_SECONDS) + "です")
    for n in range(RECORD_NUMBER):
        print(str(n+1) + "回目：検出中……………")

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            # convert data
            np_data = np.frombuffer(data, dtype="int16") / 32768.0
            # print("mean: ", np.mean(np_data))
            # print("max:  ", np.max(np_data))
            fft = np.fft.fft(np_data)
            # axis_x = np.fft.fftfreq(len(fft), d=1.0 / RATE)
            # print(fft.shape, axis_x.shape)
            amplitude_spectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]

            threshold1 = util.Threshold.threshold1  # CAN BE CHANGED
            threshold2 = util.Threshold.threshold2  # CAN BE CHANGED
            is_threshold_over = False
            sound_range = amplitude_spectrum[start:end]

            if max(np_data) > threshold1 and np.mean(sound_range) > threshold2:
                is_threshold_over = True

            tmp.append(is_threshold_over)
            tmp.pop(0)  # remove the oldest element

            frames.append(data)
            if len(frames) >= 20:
                frames.pop(0)

            # whistle detection
            # CAN BE IMPROVED!!
            if 1 <= sum(tmp[7:13]) <= 4 and i >= 16:
                print("口笛らしき音声検出！！")
                # plt.plot(axis_x[start:end], amplitude_spectrum[start:end])
                # plt.axhline(y=np.mean(sound_range), color='r')
                # plt.show()
                frame = frames[5:15]
                tmp = [False for k in range(0, 20)]
                stream.close()
                now = datetime.datetime.now()

                # コマンドラインで入力を要求する
                # 1 >> ONとして保存
                # 2 >> OFFとして保存
                # 3 >> REDとして保存
                # (1 or 2)以外 >> 何もしない
                isOn = input("ON whistle:1 \nOFF whistle: 2 \nRED color?: 3 \nDiscard: others\n>>")

                if isOn == "1":
                    is_data_exist[0] = True
                    file_name = project_dir + 'on_data/' + 'on_{0:%Y%m%d%H%M%S}.wav'.format(now)
                    all_whistle[file_name] = frame
                elif isOn == "2":
                    is_data_exist[1] = True
                    file_name = project_dir + 'off_data/' + 'off_{0:%Y%m%d%H%M%S}.wav'.format(now)
                    all_whistle[file_name] = frame
                elif isOn == "3":
                    is_data_exist[2] = True
                    file_name = project_dir + 'red_data/' + '/red_{0:%Y%m%d%H%M%S}.wav'.format(now)
                    all_whistle[file_name] = frame
                else:
                    print("保存できませんでした")
                stream.close()
                print(str(n+1) + "回目の検出終了\n")
                break

    audio.terminate()
    print("データをセーブします")
    if not os.path.exists(project_dir + 'on_data') and is_data_exist[0]:
        os.mkdir(project_dir + 'on_data')
    if not os.path.exists(project_dir + 'off_data') and is_data_exist[1]:
        os.mkdir(project_dir + 'off_data')
    if not os.path.exists(project_dir + 'red_data') and is_data_exist[2]:
        os.mkdir(project_dir + 'red_data')

    for k, v in all_whistle.items():
        wave_file = wave.open(k, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(v))
        wave_file.close()


if __name__ == "__main__":
    main()