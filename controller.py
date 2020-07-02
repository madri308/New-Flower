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
from matplotlib.path import Path
import matplotlib as mpl
from PIL import Image, ImageDraw
from PIL import ImagePath  
import random
class Controller:
    allPixels = []
    promShape = []
    GP = GeneticProcessor()
    tkinterStuf = tkinterStuff()
    quantPetals = 0
    centroProm = 0
    def __init__(self, flowers):
        self.flowers = flowers
        self.mergePixels()
        self.GP.createTable(self.allPixels)
        #self.GP.showTable()
        self.createPromShape()
        self.gerPromPetals()
        self.gerPromCenter()
        #self.resultsView()
        ## Comienza el GA --------------------
        #print()
        #self.GP.showTable()
        #print()
        #self.GP.avanzarGenContinua()
        self.root = tkinter.Tk()
        self.img = np.zeros( (800,800,3),np.uint8) 
        self.contour = np.asarray(self.promShape, 'int32')
        self.originalLimits = self.getLimits()
        self.centerArea = self.getPromCentralArea()
        self.petalArea = int((self.originalLimits[1][1]-self.originalLimits[0][1])*(self.originalLimits[3][0]-self.originalLimits[2][0]))
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
        self.panel = tkinter.Label(self.root, image = imgtk)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        start_button=Button(self.root,text="Dibujar",command=self.start)
        start_button.pack()
        self.root.mainloop()  
    def start(self):
        self.drawFlower()
        self.panel.after(10,self.start)
    def getLimits(self):
        originalLimits = [[-1,-1],[-1,-1],[-1,-1],[-1,-1]] #arriba,abajo,izq,der
        for dot in self.promShape:
            x = dot[0]
            y = dot[1]
            if(y < originalLimits[0][1] or originalLimits[0][1] == -1):
                originalLimits[0] = [x,y]
            if(y > originalLimits[1][1] or originalLimits[1][1] == -1):
                originalLimits[1] = [x,y]
            if(x < originalLimits[2][0] or originalLimits[2][0] == -1 ):
                originalLimits[2] = [x,y]
            if(x > originalLimits[3][0] or originalLimits[3][0] == -1):
                originalLimits[3] = [x,y]
        return originalLimits
    def buildPetal(self):
        originalPetal = []
        for newDot in range(int(self.petalArea)):
            x = random.randint(self.originalLimits[2][0],self.originalLimits[3][0])
            y = random.randint(self.originalLimits[0][1],self.originalLimits[1][1])
            while cv2.pointPolygonTest(self.contour,(x,y),False)<0:    
                x = random.randint(self.originalLimits[2][0],self.originalLimits[3][0])
                y = random.randint(self.originalLimits[0][1],self.originalLimits[1][1])
            originalPetal.append([x,y])
        return originalPetal
    def buildCenter(self):
        center = []
        promRadio = self.getPromRadio()
        for newDot in range(int(self.centerArea)):
            x = random.randint(int(self.centroProm[0]-promRadio),int(self.centroProm[0]+promRadio))
            y = random.randint(int(self.centroProm[1]-promRadio),int(self.centroProm[1]+promRadio))
            d = math.sqrt(((x-self.centroProm[0])**2)+((y-self.centroProm[1])**2))
            while d > promRadio:    
                x = random.randint(self.originalLimits[2][0],self.originalLimits[3][0])
                y = random.randint(self.originalLimits[0][1],self.originalLimits[1][1])
                d = math.sqrt(((x-self.centroProm[0])**2)+((y-self.centroProm[1])**2))
            center.append([x,y])
        return center
    def drawFlower(self):
        #PINTA PETALOS
        angle = 360/self.quantPetals
        originalPetal = self.buildPetal()
        for petaloId in range(self.quantPetals):
            petal = self.rotateShape(originalPetal,math.radians(angle)*petaloId,self.centroProm)
            for dot in petal:
                self.img[dot[0],dot[1]] = (self.allPixels[random.randint(0,len(self.allPixels)-1)].color)
        #PINTA CENTRO
        center = self.buildCenter()
        for dot in center:
            self.img[dot[0],dot[1]] = (255,255,255)#(self.allPixels[random.randint(0,len(self.allPixels)-1)].color)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
        self.panel.configure(image = imgtk)
        self.panel.image = imgtk
    def rotateShape(self,shape,angle,origin):
        newShape = []
        ox = origin[0]
        oy = origin[1]
        for dot in shape:
            px = dot[0]
            py = dot[1]
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
                    promDots[shapeDot] = ([int((promDots[shapeDot][0]+dot[1])/(flower+1)),int((promDots[shapeDot][1]+dot[2])/(flower+1))]) 
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
    def getPromCentralArea(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].centro.area
        return (prom/len(self.flowers))+prom/len(self.flowers)*30/100
    def gerPromCenter(self):
        prom = [0,0]
        for flower in range(len(self.flowers)):
            prom[0] = prom[0] + self.flowers[flower].centroPuntos[1]
            prom[1] = prom[1] + self.flowers[flower].centroPuntos[2]
        prom[0] = prom[0]/len(self.flowers)
        prom[1] = prom[1]/len(self.flowers)
        self.centroProm = prom
    def getPromRadio(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].centro.radio
        return prom/len(self.flowers)