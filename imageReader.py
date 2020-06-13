import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinterStuff import * 


class imageReader:
    allPixels = [[None],[None],[None]]
    RGB_images = [None,None,None]
    tkinterStuf = tkinterStuff()
    def __init__(self, paths):
        for i in range(3):
            if paths[i] != '':
                self.RGB_images[i] =  cv2.cvtColor(cv2.imread(paths[i]), cv2.COLOR_BGR2RGB)
                pixels = np.array(self.RGB_images[i])
                self.allPixels[i] = pixels
    def showImage(self):
        for image in range (len(self.RGB_images)):
            if self.RGB_images[image] is not None:
                root = self.tkinterStuf.newWindow("image"+str(image))
                f = Figure()
                a = f.add_subplot(111)
                a.imshow(self.RGB_images[image])

                canvas = FigureCanvasTkAgg(f, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
                canvas.draw()
                canvas.mpl_connect('button_press_event', lambda event: self.onclick(event,image))
                canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
                toolbar.update()
                canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)   
                tkinter.mainloop()

    def onclick(self,event,image):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)
                x = int(event.xdata)
                print('color=%s, xPixel=%f, yPixel=%f, image=%i' %
                    (self.RGB_images[image][y,x], x, y,image))
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Estas afuera de la imagen. Intenta de nuevo...")

