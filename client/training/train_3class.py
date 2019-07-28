# conding: utf-8
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
# import pprint
# pprint.pprint(sys.path)

import sys, os, re, glob, argparse
import numpy as np
import tensorflow as tf
import wave
import librosa
from common import model_3class, util

rets = np.array([])

NUM_EPOCH , NUM_BATCH = 10, 32

def wave_fft(file_name):
    global rets
    wave_file = wave.open(file_name, "r")
    buf = wave_file.readframes(wave_file.getnframes())
    wave_file.close()
    buf_int = np.frombuffer(buf, dtype="int16") / 32768.0

    # only fft
    # buf_fft = np.fft.fft(buf_int) 
    # ret = [ np.sqrt(c.real ** 2 + c.imag ** 2)/util.MAX for c in buf_fft]

    # mel
    S = librosa.feature.melspectrogram(y=buf_int, sr=util.RATE, n_mels=128, hop_length=1024)
    log_S = librosa.power_to_db(S)
    ret = (log_S.reshape(-1) - util.MEDIAN) / util.MEL_DIV
    rets = np.append(rets, ret)
    # print(ret.shape, max(ret), min(ret))
    return ret

def read_data(data, fname, label):
    for f in glob.glob(fname):
        spectrum = np.asarray( wave_fft(f) )
        data.append( util.Data(spectrum, label) )

def create_train_test():
    data_train = np.array([])
    data_test = np.array([])
    for status in util.Status:
        d = []
        read_data(d, util.get_dir(status) + "*.wav", status)
        num_train = int(util.PER_TRAIN * len(d))
        data_train = np.append(data_train, d[:num_train])
        data_test = np.append(data_test, d[num_train:])
        print("  Read", status, " train:{}, test:{}".format(num_train, len(d)-num_train))
    print("Total Train:{}, Test:{}".format(len(data_train), len(data_test)))
    return data_train, data_test
    

def calc_acc(data):
    total_pred = np.array([])
    num_batch = NUM_BATCH*2
    for i in range(0, len(data), num_batch):
        batch = data[i:i+num_batch]
        batch_input = np.array([i.spectrum for i in batch], dtype=np.float32)
        batch_label = np.array([i.label.value for i in batch], dtype=np.float32)
        pred = model.get_pred(batch_input, batch_label)
        total_pred = np.concatenate([total_pred, pred])            
    return np.mean(total_pred)

if __name__=='__main__':
    print("=> read data")
    data_train, data_test = create_train_test()
    print( "MEDIAN = ", np.mean(rets) )
    print( "MAX = ", np.max(rets) )
    print( "MIN = ", np.min(rets) )
    print( "STD = ", np.std(rets))

    print("=> init model")
    model = model_3class.Model((2048, util.OUTPUT_SIZE))

    print("=> Start training")
    acc_train = calc_acc(data_train)
    acc_test = calc_acc(data_test)
    print("acc_train:{:.4f} test:{:.4f}".format(acc_train,acc_test))

    for epoch in range(NUM_EPOCH):
        print("Epoch : ",epoch)

        # update
        for i in range(0, len(data_train), NUM_BATCH):
            batch = data_train[ i:i+NUM_BATCH ]
            batch_input = np.array([i.spectrum for i in batch], dtype=np.float32)
            batch_label = np.array([i.label.value for i in batch], dtype=np.float32)
            model.update_model(batch_input,batch_label)

        acc_train = calc_acc(data_train)
        acc_test = calc_acc(data_test)
        print("acc_train:{:.4f} test:{:.4f}".format(acc_train,acc_test))

        np.random.shuffle(data_train)
        model.save_model("./model/model_3class.ckpt")
        


