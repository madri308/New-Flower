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
    GP = GeneticProcessor()
    tkinterStuf = tkinterStuff()
    def __init__(self, flowers):
        self.flowers = flowers
        #Combinacion de pixeles
        self.allPixels = self.mergePixels()
        self.allPetalPixels = self.mergePetalPixels()
        self.allCenterPixels = self.mergeCenterPixels()
        #Saca promedios para dibujar y ayudas para dibujar
        self.promShape = self.createPromShape()
        self.contour = np.asarray(self.promShape, 'int32')
        self.quantPetals = self.getPromPetals()
        self.centroProm = self.getPromCenter()
        self.originalLimits = self.getLimits()
        #areas promedio
        self.centerArea = self.getPromCentralArea()
        self.petalArea = int((self.originalLimits[1][1]-self.originalLimits[0][1])*(self.originalLimits[3][0]-self.originalLimits[2][0]))
        #Genetico
        self.GP.createTable([self.allCenterPixels,self.allPetalPixels])
        #self.GP.showTable()
        #self.GP.avanzarGenContinua()
        #Tkinter stuff
        self.root = tkinter.Tk()
        self.img = np.zeros( (800,800,3),np.uint8) 
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
        self.panel = tkinter.Label(self.root, image = imgtk)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        start_button=Button(self.root,text="Dibujar",command=self.start)
        start_button.pack()
        self.root.mainloop() 
    #INTERFAZ         
    def start(self):
        self.drawFlower()
        self.panel.after(10,self.start)
    #PARA FORMAR LA FLOR
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
                self.img[dot[0],dot[1]] = (self.allPetalPixels[random.randint(0,len(self.allPetalPixels)-1)].color)
        #PINTA CENTRO
        center = self.buildCenter()
        for dot in center:
            self.img[dot[0],dot[1]] = (self.allCenterPixels[random.randint(0,len(self.allCenterPixels)-1)].color)
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
    #COMBINACION DE PIXELES
    def mergePixels(self):
        allPixels = []
        for flower in range(len(self.flowers)): 
            allPixels = allPixels+self.flowers[flower].pixeles
        return allPixels
    def mergePetalPixels(self):
        allPetalPixels = []
        for flower in range(len(self.flowers)): 
            allPetalPixels = allPetalPixels+self.flowers[flower].petalo.pixeles
        return allPetalPixels
    def mergeCenterPixels(self):
        allCenterPixels = []
        for flower in range(len(self.flowers)): 
            allCenterPixels = allCenterPixels+self.flowers[flower].centro.pixeles
        return allCenterPixels
    #PROMEDIOS NECESARIOS
    #Promedio de los puntos del contorno
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
        return promDots
    #Promedio cantidad de petalos
    def getPromPetals(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].cantPetalos
        prom = prom//len(self.flowers)
        return prom
    #Promedio area del centro
    def getPromCentralArea(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].centro.area
        return (prom/len(self.flowers))+(prom/len(self.flowers)*30/100)
    #Promedio punto centro
    def getPromCenter(self):
        prom = [0,0]
        for flower in range(len(self.flowers)):
            prom[0] = prom[0] + self.flowers[flower].centroPuntos[1]
            prom[1] = prom[1] + self.flowers[flower].centroPuntos[2]
        prom[0] = prom[0]/len(self.flowers)
        prom[1] = prom[1]/len(self.flowers)
        return prom
    #Promedio radio de area
    def getPromRadio(self):
        prom = 0
        for flower in range(len(self.flowers)):
            prom = prom + self.flowers[flower].centro.radio
        return prom/len(self.flowers)