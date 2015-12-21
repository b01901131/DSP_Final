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
        self.predict_flag = False
        self.label_feat = [] #'''事先錄好的Feature Signal'''
        self.prediction = "安安你好"

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

        wf = wave.open("%s.wav" % filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        #MFCC_dimension = 13
        (rate,sig) = wav.read("%s.wav" % filename)
        mfcc_feat = mfcc(sig,rate)
        
        #Dump MFCC pickle file
        cPickle.dump(mfcc_feat, open("%s_mfcc_13.pkl" % filename, "wb"))
        
    
        #Pridict or Just Record only
        if self.predict_flag == True:
            #TODOs: Load MFCC Label Feature (pkl files) as self.label_feat
            self.label_feat = []
            list_of_files = glob.glob('*.pkl')[1:]  
            for filename in list_of_files:
                print filename
                self.label_feat.append(cPickle.load( open( filename, "rb" ) ))
            dtw_result = []
            dtw = DTW()
            dtw_result = [ dtw.calc_DTW(mfcc_feat, arr2) for arr2 in self.label_feat]
            for i in range(len(list_of_files)):
                print list_of_files[i], ":", dtw_result[i]
            os.remove("%s.wav" % self.file_entry.get())
            os.remove("%s_mfcc_13.pkl" % self.file_entry.get())
            self.prediction = str(list_of_files[dtw_result.index(min(dtw_result))].split("_")[0])
            self.result_label.config(text='%s' % self.prediction, fg="red")
                

    def modeSelect(self):
        if self.predict_flag == False:
            self.predict_flag = True
        else:
            self.predict_flag = False
        
    def createWidgets(self):
        self.file_label = Label(self, text="檔名：")
        self.file_label.grid(row=0, column=0)
        self.file_entry = Entry(self)
        self.file_entry.grid(row=0, column=1)

        self.second_label = Label(self, text="秒數：")
        self.second_label.grid(row=1, column=0)
        self.second_entry = Entry(self)
        self.second_entry.grid(row=1, column=1)

        self.mode_check = Checkbutton(self, text="預測模式", command=self.modeSelect)
        self.mode_check.grid(row=3, column = 2)

        self.record_label = Label(self, text="辨識結果：")
        self.record_label.grid(row=2, column=0)

        self.result_label = Label(self, text="安安你好")
        self.result_label.grid(row=2, column=1)

        #self.counter_label = Label(self, text="0")
        #self.counter_label.grid(row=4, column=1)

        self.Record = Button(self, text="錄音")
        self.Record["fg"]   = "pink"
        self.Record["command"] = self.record
        self.Record.grid(row = 3, column = 0)

        self.Quit = Button(self, text="離開")
        self.Quit["fg"]   = "red"
        self.Quit["bg"]   = "blue"
        self.Quit["command"] =  self.quit
        self.Quit.grid(row = 3, column = 1)


    
root = Tk()
app = Application(master=root)
app.master.title('Dynamic Time Warping')
app.master.maxsize(1000,400)
app.mainloop()
root.destroy()

