# conding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys, os, re, glob, argparse
import numpy as np
import tensorflow as tf
import model_3class as model
import wave
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, median,variance,stdev
from common import *

def wave_fft(file_name):
    wave_file = wave.open(file_name, "r")
    buf = wave_file.readframes(wave_file.getnframes())
    wave_file.close()
    buf_int = np.frombuffer(buf, dtype="int16") / 32768.0
    buf_fft = np.fft.fft(buf_int) 
    amplitudeSpectrum = [ np.sqrt(c.real ** 2 + c.imag ** 2)/MAX for c in buf_fft]
    return amplitudeSpectrum

def read_data(data, fname, label):
    for f in glob.glob(fname):
        spectrum = np.asarray( wave_fft(f) )
        data.append( Data(spectrum, label) )

def create_train_test():
    data_red, data_on, data_off = [], [], []
    print(" Read RED dir")
    read_data(data_red, RED_DIR+"*.wav", Status.RED)
    print(" Read ON dir")
    read_data(data_on, ON_DIR+"*.wav", Status.ON)
    print(" Read OFF dir")
    read_data(data_off, OFF_DIR+"*.wav", Status.OFF)

    num_red_train = int(PER_TRAIN * len(data_red))
    num_on_train = int(PER_TRAIN * len(data_on))
    num_off_train = int(PER_TRAIN * len(data_off))

    data_train = np.concatenate( [data_red[:num_red_train], data_on[:num_on_train], data_off[:num_off_train]] )
    data_test = np.concatenate( [data_red[num_red_train:], data_on[num_on_train:], data_off[num_off_train:]] )
    print( "RED  train:{}, test:{}".format(num_red_train, len(data_red)-num_red_train) )
    print( "ON   train:{}, test:{}".format(num_on_train, len(data_on)-num_on_train) )
    print( "OFF  train:{}, test:{}".format(num_off_train, len(data_off)-num_off_train) )
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

    print("=> init model")
    model = model.Model((DATA_LEN,OUTPUT_SIZE))

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
        


