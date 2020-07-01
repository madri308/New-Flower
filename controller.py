from flowerComponents import *
from geneticOperator import *
from geneticProcessor import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinterStuff import *  
import math
import cv2
class Controller:
    allPixels = []
    promShape = []
    GP = GeneticProcessor()
    tkinterStuf = tkinterStuff()
    quantPetals = 0
    centroProm = 0
    def __init__(self, flowers):
        self.flowers = flowers
        #self.mergePixels()
        #self.GP.createTable(self.allPixels)
        self.createPromShape()
        self.gerPromPetals()
        self.gerPromCenter()
        self.resultsView()
    def resultsView(self):
        """root = self.tkinterStuf.newWindow("resultado")
        root.configure(bg='white')

        f = Figure()
        a = f.add_subplot(111)
        a.imshow(self.RGB_images[imageID])
                
        canvas = FigureCanvasTkAgg(f, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
        canvas.draw()
        tkinter.mainloop()"""
        contours = np.asarray(self.promShape, 'int32')
        img = np.zeros( (800,800) ) 
        angleOriginal = 360/self.quantPetals
        for petalo in range(self.quantPetals+1):
            contours = self.rotateShape(contours,math.radians(angleOriginal),self.centroProm)
            cv2.fillConvexPoly(img, contours, (255,255,255),lineType=4)
        cv2.imshow(" ", img)
        cv2.waitKey()
    def rotateShape(self,shape,angle,origin):
        newShape = []
        for dot in shape:
            px = dot[0]
            py = dot[1]
            ox = origin[0]
            oy = origin[1]
            nx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            ny = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            newShape.append([nx,ny])
        return np.asarray(newShape, 'int32')

    def mergePixels(self):
        for flower in range(len(self.flowers)): 
            self.allPixels = self.allPixels+self.flowers[flower].pixeles
    def createPromShape(self):
        quantDots =len(self.flowers[0].petalo.contorno)
        promDots = [[0,0]]*quantDots 
        for flower in range(len(self.flowers)):
            for shapeDot in range(len(self.flowers[flower].petalo.contorno)):
                dot = self.flowers[flower].petalo.contorno[shapeDot]
                if flower == len(self.flowers)-1:
                    promDots[shapeDot] = ([(promDots[shapeDot][0]+dot[1])/(flower+1),(promDots[shapeDot][1]+dot[2])/(flower+1)]) 
                else:
                    promDots[shapeDot] = ([(promDots[shapeDot][0]+dot[1]),(promDots[shapeDot][1]+dot[2])]) 
        self.promShape = promDots
    def getPromShape(self):
        for shapeDot in range(len(self.promShape)):
            print(self.promShape[shapeDot][0]," ",self.promShape[shapeDot][1])
    def gerPromPetals(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].cantPetalos
        prom = prom//len(self.flowers)
        self.quantPetals = prom
    def gerPromCenter(self):
        prom = [0,0]
        for flower in range(len(self.flowers)):
            prom[0] = prom[0] + self.flowers[flower].centro[1]
            prom[1] = prom[1] + self.flowers[flower].centro[2]
        prom[0] = prom[0]/len(self.flowers)
        prom[1] = prom[1]/len(self.flowers)
        self.centroProm = prom