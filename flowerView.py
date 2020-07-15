from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinterStuff import *  
from controller import *      
from flowerComponents import *
import math
import cv2

class FlowerView:
    RGB_images = []
    importantDots = [[],[],[]]
    tkinterStuf = tkinterStuff()
    flowers = []
    def __init__(self, rgbImages):
        self.fila = 0 #Saber la ultima fila correspondiente a los puntos para poder borrarla.
        #FILTRA LAS IMAGENES QUE ME LLEGARON PARA SOLO OBTENER LAS QUE NO SON NULAS(EN CASO DE QUE SEAN MENOS DE 3 IMAGENES)
        for i in range(3):
            if rgbImages[i] is not None:
                self.RGB_images.append(rgbImages[i]) 
        self.showImage()
    def showImage(self):
        #RECORRE LAS 3 IMAGENES
        for imageID in range (len(self.RGB_images)):
            #CONFIGURACION DE LA VENTANA DONDE SE MOSTRARA LA IMAGEN
            root = self.tkinterStuf.newWindow("image"+str(imageID))
            root.configure(bg='white')
            #FRAME DONDE SE MOSTRARAN LOS PUNTOS Y SUS CARACTERISTICAS
            left_frame = tkinter.Frame(root)
            left_frame.pack(sid="left")
            left_frame.configure(bg='white')
            #TEXTO SOBRE INDICACIONES 
            infoDots = Label(root, text="Puntos: minimo 10 en el siguiente orden:\n1. Un color petalos."+
                                                            "\n2. Un color centro."+
                                                            "\n3. Un centro de la flor."+
                                                            "\n4. Un contorno del centro."+
                                                            "\n5. Un extremo de un petalo."+
                                                            "\n6. Cinco o más del contorno de un petalo. (direccion reloj)"+
                                                            "\n Y por favor abajo ingrese la cantidad de colores de la imagen.",justify=tkinter.LEFT)
            infoDots.pack(sid="top")
            #SE GENERA UN OBJETO FIGURA PARA MOSTRAR LA IMAGEN, CONVIENE A LA HORA DE OBTENER PUNTOS
            f = Figure()
            a = f.add_subplot(111)
            a.imshow(self.RGB_images[imageID])
            #CREA UN AREA DE DIBUJO EN TKINTER PARA INSERTAR EL OBJETO CON LA IMAGEN
            canvas = FigureCanvasTkAgg(f, master=root) 
            canvas.draw()
            #METODO PARA CONSEGUIR PUNTOS DONDE EL USER HAGA CLICK
            canvas.mpl_connect('button_press_event', lambda event: self.onclick(event,imageID,left_frame))
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
            toolbar.update()
            canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)  
            #ENTRY BOX PARA CONSEGUIR LA CANTIDAD DE PUNTOS DADA POR EL USUARIO (PARA VORAZ)
            quantUniqueColors = tkinter.Entry(root,justify=tkinter.CENTER,width = 15)
            quantUniqueColors.pack(side = tkinter.BOTTOM)
            #BOTON PARA ELIMINAR EL ULTIMO PUNTO QUE SE GUARDO
            deleteRowButton = tkinter.Button(root, text="Eliminar ultimo punto", command=lambda:self.deleteLastRow(imageID,left_frame))
            deleteRowButton.pack(sid="bottom")
            #BOTON PARA GUARDAR LA INFO Y SEGUIR YA SEA CON LA OTRA IMAGEN O CON EL DIBUJADO DE LA NUEVA FLOR
            saveData = tkinter.Button(root, text="Siguiente", command=lambda:self.next(imageID,root,quantUniqueColors.get()))
            saveData.pack(sid="bottom")

            tkinter.mainloop()
            self.fila = 0 #SE VUELVE FILA A 0 YA QUE EMPIEZA EL PROCESO DE UNA NUEVA IMAGEN
    #GUARDA LOS PUNTOS DONDE EL USUARIO HIZO CLICK
    def onclick(self,event,imageID,left_frame):
        try:
            if event.ydata is not None or event.xdata is not None:
                y = int(event.ydata)#Y DONDE SE HIZO CLICK EN LA IMAGEN
                x = int(event.xdata)#X DONDE SE HIZO CLICK EN LA IMAGEN 
                #SE CREA UNA LISTA CON LA INFORMACION DEL PUNTO [COLOR,X,Y,NUMERO DE PUNTO]
                infoOfDot = [self.RGB_images[imageID][y,x], x, y,self.fila]
                #SE GUARDA LA INFORMACION DEL PUNTO EN UNA LISTA DE PUNTOS IMPORTANTES CORRESPONDIENTES A LA IMAGEN
                self.importantDots[imageID].append(infoOfDot) 
                #ACTUALIZA EL FRAME DONDE SE MUESTAN LOS PUNTOS Y SUS DATOS
                for dato in range (4): #4 PORQUE SON 4 DATOS IMPORTANTES DEL PUNTO
                    cell = tkinter.Entry(left_frame, width=11, fg='black', font=('Arial',10),bg='white')
                    cell.grid(row=self.fila, column=dato) 
                    cell.insert(END, (self.importantDots[imageID])[self.fila][dato])  
                self.fila = self.fila+1#se incrementa la fila ya que sigue otro punto abajo
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops!  Estas afuera de la imagen. Intenta de nuevo...")
    #ELIMINA LA INFO DEL ULTIMO PUNTO
    def deleteLastRow(self,imageID,left_frame):
        try:
            if len(self.importantDots[imageID]) != 0: 
                self.importantDots[imageID].pop()#Saca al ultimo punto de la lista
                #elimina las ultimas 4 celdas insertadas en el frame
                for elemento in range(4):
                    grids = left_frame.grid_slaves()
                    grids[0].destroy()
                self.fila = self.fila-1#decrementa la fila para que el siguiente punto quede en la pos donde estaba este
            else:
                raise ValueError
        except ValueError:
            self.tkinterStuf.showError("Oops! Ya no hay puntos.")
    def next(self,imageID,root,entryUniqueColors):
        #deben haber al menos 10 puntos
        if len(self.importantDots[imageID]) < 10 or entryUniqueColors == "":
            self.tkinterStuf.showError("Oops! Te faltan datos.")#sino muestra un error
        else:
            root.title("Pocesando...")
            #CREA UNA FLOR CON LOS DATOS CORRESPONDIENTES(IMAGEN, PUNTOS, ID, CANTIDAD DE COLORES)
            flor = Flor(image=self.RGB_images[imageID],dots=self.importantDots[imageID],imageID=imageID,uniqueColors = int(entryUniqueColors))
            #VA GUARDANDO LAS FLORES EN UNA LISTA
            self.flowers.append(flor)
            root.quit()
            root.destroy() 
            #CUANDO YA ESTAMOS EN LA FLOR FINAL
            if(imageID == len(self.RGB_images)-1):
                #VAMOS A LO BONITO
                controller = Controller(self.flowers) 

