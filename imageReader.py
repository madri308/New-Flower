import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinterStuff import * 


class imageReader:
    pixels = []
    tkinterStuf = tkinterStuff()
    def __init__(self, url):
        self.url = url
        img = cv2.imread(self.url)
        self.RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.pixels = np.array(self.RGB_img)
    def showImage(self):
        root = self.tkinterStuf.newWindow("New Flower")

        f = Figure()
        a = f.add_subplot(111)
        a.imshow(self.RGB_img)
        

        canvas = FigureCanvasTkAgg(f, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
        canvas.draw()
        canvas.mpl_connect('button_press_event', self.onclick)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)   
        tkinter.mainloop()

    def onclick(self,event):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)
                x = int(event.xdata)
                print('color=%s, xPixel=%f, yPixel=%f' %
                    (self.RGB_img[y,x], x, y))
                print(self.pixels[2][2])
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Estas afuera de la imagen. Intenta de nuevo...")

