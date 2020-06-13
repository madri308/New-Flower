import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinterStuff import * 
import math


class flowerView:
    allPixels = [[None],[None],[None]]
    RGB_images = [None,None,None]
    importantDots = [[],[],[]]
    tkinterStuf = tkinterStuff()
    def __init__(self, rgbImages):
        self.indice = 0
        for i in range(3):
            if rgbImages[i] is not None:
                self.RGB_images[i] =  rgbImages[i]
                pixels = np.array(self.RGB_images[i])
                self.allPixels[i] = pixels
        self.showImage()
    def showImage(self):
        for image in range (len(self.RGB_images)):
            if self.RGB_images[image] is not None:
                root = self.tkinterStuf.newWindow("image"+str(image))
                root.configure(bg='white')

                left_frame = tkinter.Frame(root)
                left_frame.pack(sid="left")
                left_frame.configure(bg='white')

                
                infoDots = Label(root, text="Puntos: usted tiene 9 puntos, los primeros 2 para indicar colores\n"+
                                                    "de los petalos que le gusten, los siguientes 2 para colores del\n"+
                                                    "centro que le gusten, los siguientes 5 para marcar el centro y el\n"+
                                                    "contorno del centro y los ultimos 5 para marcar el contorno de un petalo.")
                infoDots.pack(sid="top")

                f = Figure()
                a = f.add_subplot(111)
                a.imshow(self.RGB_images[image])
                  
                canvas = FigureCanvasTkAgg(f, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
                canvas.draw()
                canvas.mpl_connect('button_press_event', lambda event: self.onclick(event,image,left_frame))
                canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
                toolbar.update()
                canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)  
                deleteRowButton = tkinter.Button(root, text="Eliminar ultimo punto", command=lambda:self.deleteLastRow(image,left_frame))
                deleteRowButton.pack(sid="bottom")
                tkinter.mainloop()
            self.indice = 0
    def onclick(self,event,image,left_frame):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)
                x = int(event.xdata)
                infoOfDot = [self.RGB_images[image][y,x], x, y]
                self.importantDots[image].append(infoOfDot) 
                for dato in range (3):
                    e = tkinter.Entry(left_frame, width=11, fg='black', font=('Arial',10),bg='white')
                    e.grid(row=self.indice, column=dato) 
                    e.insert(END, (self.importantDots[image])[self.indice][dato])  

                self.indice = self.indice+1
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Estas afuera de la imagen. Intenta de nuevo...")
    def deleteLastRow(self,image,left_frame):
        try:
            if len(self.importantDots[image]) != 0: 
                print(self.importantDots[image])
                self.importantDots[image].pop()
                print(self.importantDots[image])
                for elementos in range(3):
                    grids = left_frame.grid_slaves()
                    grids[0].destroy()
                self.indice = self.indice-1
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Ya no hay puntos.")

