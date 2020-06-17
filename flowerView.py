from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinterStuff import *        
from flowerComponents import *
import math
import cv2

class FlowerView:
    allPixels = []
    RGB_images = []
    importantDots = [[],[],[]]
    tkinterStuf = tkinterStuff()
    def __init__(self, rgbImages):
        self.fila = 0
        for i in range(3):
            if rgbImages[i] is not None:
                self.RGB_images.append(rgbImages[i]) 
                pixels = np.array(self.RGB_images[i])
                self.allPixels.append(pixels)
        self.showImage()
    def showImage(self):
        for imageID in range (len(self.RGB_images)):
            root = self.tkinterStuf.newWindow("image"+str(imageID))
            root.configure(bg='white')

            left_frame = tkinter.Frame(root)
            left_frame.pack(sid="left")
            left_frame.configure(bg='white')

            infoDots = Label(root, text="Puntos: minimo 10 puntos.\n- 1 Color petalos."+
                                                            "\n- 1 Color centro."+
                                                            "\n- 1 Centro de la flor."+
                                                            "\n- 1 Contorno del centro."+
                                                            "\n- 1 Extremo de un petalo."+
                                                            "\n- 5 o más Contorno de un petalo. (direccion reloj)",justify=tkinter.CENTER)
            infoDots.pack(sid="top")

            f = Figure()
            a = f.add_subplot(111)
            a.imshow(self.RGB_images[imageID])
                
            canvas = FigureCanvasTkAgg(f, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
            canvas.draw()
            canvas.mpl_connect('button_press_event', lambda event: self.onclick(event,imageID,left_frame))
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
            toolbar.update()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)  
            deleteRowButton = tkinter.Button(root, text="Eliminar ultimo punto", command=lambda:self.deleteLastRow(imageID,left_frame))
            deleteRowButton.pack(sid="bottom")
            saveData = tkinter.Button(root, text="Siguiente", command=lambda:self.next(imageID,root))
            saveData.pack(sid="bottom")
            tkinter.mainloop()
            self.fila = 0
    def onclick(self,event,imageID,left_frame):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)
                x = int(event.xdata)
                infoOfDot = [self.RGB_images[imageID][y,x], x, y,self.fila]
                self.importantDots[imageID].append(infoOfDot) 
                for dato in range (4):
                    e = tkinter.Entry(left_frame, width=11, fg='black', font=('Arial',10),bg='white')
                    e.grid(row=self.fila, column=dato) 
                    e.insert(END, (self.importantDots[imageID])[self.fila][dato])  

                self.fila = self.fila+1
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Estas afuera de la imagen. Intenta de nuevo...")
    def deleteLastRow(self,imageID,left_frame):
        try:
            if len(self.importantDots[imageID]) != 0: 
                self.importantDots[imageID].pop()
                for elemento in range(4):
                    grids = left_frame.grid_slaves()
                    grids[0].destroy()
                self.fila = self.fila-1
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops! Ya no hay puntos.")
    def next(self,imageID,root):
        if len(self.importantDots[imageID]) < 10:
            self.tkinterStuf.showError("Oops! Te faltan puntos.")
        else:
            root.quit()
            root.destroy() 
            flor = Flor(image=self.RGB_images[imageID],dots=self.importantDots[imageID],imageID=imageID)

