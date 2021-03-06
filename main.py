from imageReader import * 
from flowerView import *
import PIL.Image, PIL.ImageTk
import os
class MainApplication(tkinter.Frame):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #CONFIGURACION DE LA VENTANA
        root.geometry("500x200")
        root.configure(bg='white')
        root.wm_title("New Flower")
        root.resizable(False,False)
        #ENTRY BOX PARA METER LOS PATHS DE LAS IMAGENES
        entry3 = tkinter.Entry(root,justify=tkinter.CENTER,width = 70)
        entry3.pack(side = tkinter.BOTTOM)
        entry2 = tkinter.Entry(root,justify=tkinter.CENTER,width = 70)
        entry2.pack(side = tkinter.BOTTOM)
        entry1 = tkinter.Entry(root,justify=tkinter.CENTER,width = 70)
        entry1.pack(side = tkinter.BOTTOM)
        #BOTON PARA EMPEZAR
        start = tkinter.Button(root, text="Empezar", command=lambda:self.callback([entry1.get(),entry2.get(),entry3.get()]))
        start.pack(side = tkinter.BOTTOM)
        #CODIGO PARA LA IMAGEN DE LA VENTANA PRINCIPAL
        cv_img = cv2.cvtColor(cv2.imread("C:/Users/emema/Documents/TEC/2020/SEM_I/Analisis/New-Flower/images/logo.png"),cv2.COLOR_BGR2RGB)
        height, width, no_channels = cv_img.shape
        canvas = tkinter.Canvas(root, width = width, height = height)
        canvas.pack()
        self.background = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))   
        canvas.create_image(0, 0, image=self.background, anchor=tkinter.NW)
        
    def callback(self,paths): 
        #GUARDA LAS IMAGENES Y LAS MANDA A FLOWER VIEW DONDE SERAN MOSTRADAS
        reader = ImageReader(paths)
        rgbImages = reader.getResults()
        root.quit()
        root.destroy() 
        view = FlowerView(rgbImages)

if __name__ == "__main__":
    #SE CREA VENTANA PRINCIPAL 
    root = tkinter.Tk()
    MainApplication(root).pack(side="left", fill="both", expand=False)
    root.mainloop()
    