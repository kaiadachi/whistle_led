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
    project_dir = os.getcwd() + "/training"

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
    # 3 >> REDとして保存
    # (1 or 2)以外 >> 何もしない
    isOn = input("ON whistle:1 \nOFF whistle: 2 \nRED color?: 3 \nDiscard: others\n>>")

    if isOn == "1":
        file_name = project_dir + 'on_data/' + 'on_{0:%Y%m%d%H%M%S}.wav'.format(now)
    elif isOn == "2":
        file_name = project_dir + 'off_data/' + 'off_{0:%Y%m%d%H%M%S}.wav'.format(now)
    elif isOn == "3":
        file_name = project_dir + 'red_data/' + '/red_{0:%Y%m%d%H%M%S}.wav'.format(now)
    else:
        print("保存できませんでした")
        return

    if not os.path.exists(project_dir + 'on_data') and isOn == "1":
        os.mkdir(project_dir + 'on_data')
    if not os.path.exists(project_dir + 'off_data') and isOn == "2":
        os.mkdir(project_dir + 'off_data')
    if not os.path.exists(project_dir + 'red_data') and isOn == "3":
        os.mkdir(project_dir + 'red_data')

    waveFile = wave.open(file_name, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

if __name__ == "__main__":
    main()