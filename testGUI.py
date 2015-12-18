from Tkinter import *
from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav
import pyaudio
import wave
import cPickle

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

class Application(Frame):
    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        (rate,sig) = wav.read("output.wav")
        mfcc_feat = mfcc(sig,rate)
        
        cPickle.dump(mfcc_feat, open("mfcc_13_output.pkl", "wb"))
        
    def createWidgets(self):
        self.Quit = Button(self)
        self.Quit["text"] = "Quit"
        self.Quit["fg"]   = "red"
        self.Quit["bg"]   = "blue"
        self.Quit["command"] =  self.quit
        self.Quit.grid(row = 0, column = 0)

        self.Record = Button(self)
        self.Record["text"] = "Record"
        self.Record["fg"]   = "pink"
        self.Record["command"] = self.record
        self.Record.grid(row = 1, column = 0)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title('Dynamic Time Warping')
app.master.maxsize(1000,400)
app.mainloop()
root.destroy()

