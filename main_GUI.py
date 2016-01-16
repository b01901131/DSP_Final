#!/usr/bin/python
# -*- coding: utf8 -*-
from Tkinter import *
from features import mfcc
from features import logfbank
from DTW import *
import scipy.io.wavfile as wav
import pyaudio
import wave
import cPickle
import glob
import os
import argparse


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.record_seconds = 3 #'''每筆音訊都是三秒'''
        self.no_cluster = False
        self.hac = False
        self.k_means = False
        self.label_feat = [] #'''事先錄好的Feature Signal'''
        self.prediction = "安安你好"
        self.dtw = DTW()
            

    def record(self):
        #start Recording...
        self.record_seconds = int(self.second_entry.get())
        if self.file_entry.get() == "":
            filename = "output"
        else:
            filename = self.file_entry.get()
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * self.record_seconds)):
            #if i % 60 == 0:
            #    self.counter_label.config(text="%i" % i)
            print i / 42.0
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open("model_%s/%s.wav" % (SETS,filename), 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        #MFCC_dimension = 13
        (rate,sig) = wav.read("model_%s/%s.wav" % (SETS,filename))
        #Dump MFCC pickle file
        mfcc_feat = mfcc(sig,rate)
        cPickle.dump(mfcc_feat, open("model_%s/%s.mfcc" % (SETS,filename), "wb"))
        #Dump HAC pickle file
        hac_feat = self.dtw.calc_HAC(mfcc_feat)
        cPickle.dump(hac_feat, open("model_%s/%s.hac" % (SETS,filename), "wb"))
        #Dump K-means pickle file
        k_means_feat = self.dtw.calc_Kmeans(mfcc_feat)
        cPickle.dump(k_means_feat, open("model_%s/%s.kmeans" % (SETS,filename), "wb"))
    
        #Pridict or Just Record only
        if self.no_cluster or self.hac or self.k_means:
            start_time = time.time()
            #TODOs: Load MFCC Label Feature (pkl files) as self.label_feat
            self.label_feat = []
            if not self.hac and not self.k_means:
                list_of_files = glob.glob('model_%s/*.mfcc' % SETS)[1:]  
                for filename in list_of_files:
                    self.label_feat.append(cPickle.load( open( filename, "rb" ) ))
                dtw_result = [ self.dtw.calc_DTW(mfcc_feat, arr2) for arr2 in self.label_feat]
            #    for i in range(len(list_of_files)):
            #        print list_of_files[i], ":", dtw_result[i]
            elif self.hac and not self.k_means:
                print "HAC"
                list_of_files = glob.glob('model_%s/*.hac' % SETS)[1:]  
                for filename in list_of_files:
                    self.label_feat.append(cPickle.load( open( filename, "rb" ) ))
                dtw_result = [ self.dtw.calc_DTW(hac_feat, arr2) for arr2 in self.label_feat]
            #    for i in range(len(list_of_files)):
            #        print list_of_files[i], ":", dtw_result[i]
            elif self.k_means and not self.hac:
                print "K-means"
                list_of_files = glob.glob('model_%s/*.kmeans' % SETS)[1:]  
                for filename in list_of_files:
                    self.label_feat.append(cPickle.load( open( filename, "rb" ) ))
                dtw_result = [ self.dtw.calc_DTW(k_means_feat[0], arr2[0]) for arr2 in self.label_feat]
            #    for i in range(len(list_of_files)):
            #        print list_of_files[i], ":", dtw_result[i]
            self.prediction = str(list_of_files[dtw_result.index(min(dtw_result))].split(".")[0][9:])
            self.result_label.config(text='%s' % self.prediction, fg="red")
            elapsed_time = time.time() - start_time
            self.counter_label.config(text="DTW時間: %.2f" % elapsed_time)
            
            os.remove("model_%s/%s.wav" % (SETS, self.file_entry.get()))
            os.remove("model_%s/%s.mfcc" % (SETS, self.file_entry.get()))
            os.remove("model_%s/%s.hac" % (SETS, self.file_entry.get()))
            os.remove("model_%s/%s.kmeans" % (SETS, self.file_entry.get()))
                    
                

    def modeSelect(self, mode):
        if self.no_cluster == False and mode == "mfcc" :
            self.no_cluster = True
            self.hac = False
            self.k_means = False
        else:
            self.no_cluster = False
        if self.hac == False and mode == "hac":
            print "HAC"
            self.no_cluster = False
            self.hac = True
            self.k_means = False
        else:
            self.hac = False
        if self.k_means == False and mode == "k-means":
            print "k_means"
            self.no_cluster = False
            self.hac = False
            self.k_means = True
        else:
            self.k_means = False

    def createWidgets(self):
        self.file_label = Label(self, text="檔名：")
        self.file_label.grid(row=0, column=0)
        self.file_entry = Entry(self)
        self.file_entry.grid(row=0, column=1)

        self.second_label = Label(self, text="秒數：")
        self.second_label.grid(row=1, column=0)
        self.second_entry = Entry(self)
        self.second_entry.grid(row=1, column=1)

        self.mode_check = Checkbutton(self, text="DTW", command=lambda: self.modeSelect("mfcc"))
        self.mode_check.grid(row=0, column = 2)
        self.mode_check = Checkbutton(self, text="DTW(HAC)", command=lambda: self.modeSelect("hac"))
        self.mode_check.grid(row=1, column = 2)

        self.mode_check = Checkbutton(self, text="DTW(K-means)", command=lambda: self.modeSelect("k-means"))
        self.mode_check.grid(row=2, column = 2)


        self.record_label = Label(self, text="辨識結果：")
        self.record_label.grid(row=2, column=0)

        self.result_label = Label(self, text="安安你好")
        self.result_label.grid(row=2, column=1)

        self.counter_label = Label(self, text="DTW時間: %.2f" % 0.0)
        self.counter_label.grid(row=4, column=1)

        self.Record = Button(self, text="錄音")
        self.Record["fg"]   = "pink"
        self.Record["command"] = self.record
        self.Record.grid(row = 3, column = 0)

        self.Quit = Button(self, text="離開")
        self.Quit["fg"]   = "red"
        self.Quit["bg"]   = "blue"
        self.Quit["command"] =  self.quit
        self.Quit.grid(row = 3, column = 1)

parser = argparse.ArgumentParser()
parser.add_argument('-cluster', type=str, default='15')
args = parser.parse_args()
SETS = args.cluster
root = Tk()
app = Application(master=root)
app.master.title('Dynamic Time Warping')
app.master.maxsize(1000,400)
app.mainloop()
root.destroy()

