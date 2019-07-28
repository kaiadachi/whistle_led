import datetime
import os
import sys
import time
import pyaudio
import wave

if len(sys.argv) == 2:
    RECORD_SECONDS = int(sys.argv[1])
else:
    RECORD_SECONDS = 1


def main():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = int(RATE/10)
    project_dir = os.getcwd() + "/"

    audio = pyaudio.PyAudio()

    # start Recording
    print("録音を始めます。" + str(RECORD_SECONDS) + "秒間です")
    time.sleep(0.1)
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("録音を終了します")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    now = datetime.datetime.now()
    # コマンドラインで入力を要求する
    # 1 >> ONとして保存
    # 2 >> OFFとして保存
    # 3 >> CHANGEとして保存
    # (1 or 2)以外 >> 何もしない
    isOn = input("ON whistle:1 \nOFF whistle: 2 \nCHANGE color?: 3 \nDiscard: others\n>>")

    if isOn == "1":
        file_name = project_dir + 'whistle_on_' + str(int(RATE)) + '/on_{0:%Y%m%d%H%M%S}.wav'.format(now)
    elif isOn == "2":
        file_name = project_dir + 'whistle_off_' + str(int(RATE)) + '/off_{0:%Y%m%d%H%M%S}.wav'.format(now)
    elif isOn == "3":
        file_name = project_dir + 'whistle_change_' + str(int(RATE)) + '/change_{0:%Y%m%d%H%M%S}.wav'.format(now)
    else:
        print("保存できませんでした")
        return

    # if not os.path.exists(project_dir + 'sounds'):
    #     os.mkdir(project_dir + "sounds")
    if not os.path.exists(project_dir + 'whistle_on_' + str(int(RATE))) and isOn == "1":
        os.mkdir(project_dir + 'whistle_true_' + str(int(RATE)))
    if not os.path.exists(project_dir + 'whistle_off_' + str(int(RATE))) and isOn == "2":
        os.mkdir(project_dir + 'whistle_false_' + str(int(RATE)))
    if not os.path.exists(project_dir + 'whistle_change_' + str(int(RATE))) and isOn == "3":
        os.mkdir(project_dir + 'whistle_change_' + str(int(RATE)))

    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

if __name__ == "__main__":
    main()