from tkinterStuff import *  
from PIL import Image, ImageDraw
import numpy as np
#from controller import *
class resultView:
    def __init__(self,controller):
        self.controller = controller
        self.root = tkinter.Tk()
        self.root.resizable(False,False)
        frame = tkinter.Frame(self.root)
        frame.pack(side = "top")

        self.img = np.zeros( (600,600,3),np.uint8) 
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
        self.imagePanel = tkinter.Label(self.root, image = imgtk)
        self.imagePanel.pack(side = "left", fill = "both", expand = "yes")
        self.OGimagePanel = tkinter.Label(self.root, image = imgtk)
        self.OGimagePanel.pack(side = "left", fill = "both", expand = "yes")

        self.start_button=Button(frame,text="Dibujar 1",command=lambda:self.setMode(0))
        self.start_button.pack(side = "left")
        self.start_button2=Button(frame,text="Dibujar 2",command=lambda:self.setMode(1))
        self.start_button2.pack(side = "left")
        self.stop_button=Button(frame,text="Pausar",command=self.stop)
        self.restart_button=Button(frame,text="Seguir",command=self.restart)
    def setMode(self,mode):
        self.start_button.pack_forget()
        self.start_button2.pack_forget()
        self.stop_button.pack(side = "left")
        self.restart_button.pack(side = "left")
        self.controller.setMode(mode)
    def stop(self):
        self.controller.stop()
    def start(self):
        self.controller.start()
    def restart(self):
        self.controller.restart()
    def show(self):
        self.root.mainloop() 
