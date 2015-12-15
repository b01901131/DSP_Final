from Tkinter import *


class Application(Frame):
    def say_hi(self):
        #print "hi there, everyone!"
        print self.QUIT.config('highlightthickness')
        

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["bg"]   = "blue"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello"
        self.hi_there["fg"]   = "pink"
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left", "expand": 1})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title('FUCK You BItch!')
app.master.maxsize(1000,400)
app.mainloop()
root.destroy()

