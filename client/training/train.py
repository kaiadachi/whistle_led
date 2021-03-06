# conding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys, os, re, glob, argparse
import numpy as np
import tensorflow as tf
import model as model
import wave
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, median,variance,stdev
from common import *

ave_var = []

def wave_fft(file_name):
    wave_file = wave.open(file_name, "r")
    buf = wave_file.readframes(wave_file.getnframes())
    wave_file.close()
    buf_int = np.frombuffer(buf, dtype="int16") / 32768.0
    buf_fft = np.fft.fft(buf_int) 
    # axis_x = np.fft.fftfreq(len(buf_fft), d=1.0/RATE)
    # plt.plot(axis_x, buf_fft)
    # amplitudeSpectrum = [ np.sqrt(c.real ** 2 + c.imag ** 2) for c in buf_fft]
    amplitudeSpectrum = [ np.sqrt(c.real ** 2 + c.imag ** 2)/util.MAX for c in buf_fft]
    ave_var.extend(amplitudeSpectrum)
    # plt.plot(axis_x, amplitudeSpectrum)
    # plt.show()

    return amplitudeSpectrum

def read_data(data, fname, label):
    # cnt = 0
    for f in glob.glob(fname):
        spectrum = np.asarray( wave_fft(f) )
        data.append( Data(spectrum, label) )
        # cnt += 1
        # if cnt>10:
            # break

def create_train_test():
    data_t, data_f = [], []
    print("True data")
    read_data(data_t,ON_DIR+"*.wav", 1.0)
    print("false data")
    read_data(data_f,OFF_DIR+"*.wav", 0.0)

    num_t_train = int(PER_TRAIN * len(data_t))
    num_f_train = int(PER_TRAIN * len(data_f))
    data_train = np.concatenate( [data_t[:num_t_train], data_f[:num_f_train]] )
    data_test = np.concatenate( [data_t[num_t_train:], data_f[num_f_train:]] )    
    print("True  train:{}, test:{}".format(num_t_train,len(data_t)-num_t_train))
    print("False train:{}, test:{}".format(num_f_train,len(data_f)-num_f_train))
    print("Total Train:{}, Test:{}".format(len(data_train), len(data_test)))

    return data_train, data_test
    

def calc_acc(data):
    total_pred = np.array([])
    num_batch = NUM_BATCH*2
    for i in range(0, len(data), num_batch):
        batch = data[i:i+num_batch]
        batch_input = np.array([i.spectrum for i in batch], dtype=np.float32)
        batch_label = np.array([i.label for i in batch], dtype=np.float32)[:,np.newaxis]
        pred = model.get_pred(batch_input, batch_label)
        total_pred = np.concatenate([total_pred, pred[:,0]], axis=0)            
    return np.mean(total_pred)

if __name__=='__main__':
    print("=> read data")
    data_train, data_test = create_train_test()
    # print("MAX = ", max(ave_var))
    # print("AVERAGE = ", mean(ave_var))
    # print("MEDIAN = ", median(ave_var))

    print("=> init model")
    model = model.Model((DATA_LEN))


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
            batch_label = np.array([i.label for i in batch], dtype=np.float32)[:,np.newaxis]
            model.update_model(batch_input,batch_label)

        acc_train = calc_acc(data_train)
        acc_test = calc_acc(data_test)
        print("acc_train:{:.4f} test:{:.4f}".format(acc_train,acc_test))

        np.random.shuffle(data_train)
        model.save_model("./model/model_on_off.ckpt")
        


