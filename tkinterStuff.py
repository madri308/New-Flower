import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk
from PIL import Image

class tkinterStuff():
    def newWindow(self, title):
        root = tkinter.Tk()
        root.wm_title(title)
        return root
    def showError(self,error):
        messagebox.showerror("Error",error)
    
        

    
