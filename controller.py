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
from resultView import *  
from IConstant import IConstant

class Controller(IConstant):
    tkinterStuf = tkinterStuff()
    def __init__(self, flowers):
        self.state = 1
        self.mode = 0
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
        self.originalLimits = self.getLimits()#Limites para pintar pixeles de un petalo, forma un rectangulo alrededor del petalo
        #areas promedio
        self.centerArea = self.getPromCentralArea()
        #En realidad es el area del rectangulo que encierra al petalo para que no falten puntos
        self.petalArea = int((self.originalLimits[1][1]-self.originalLimits[0][1])*(self.originalLimits[3][0]-self.originalLimits[2][0]))
        #Genetico
        self.GP = GeneticProcessor()
        self.GP.createTable([self.allCenterPixels,self.allPetalPixels])
        #Tkinter stuff
        self.view = resultView(self)
        self.view.show()
    #INTERFAZ      
    #Establece que modo de pintado se usara, y adecua los datos a cada modo
    def setMode(self,mode):
        if mode == 1:
            #A punta de pruebas notamos que 
            self.quantPetals = self.quantPetals//2#La mitad de los petalos representaban mas la cantidad real 
            self.petalArea = (self.petalArea*20//100)#El 20% de pixeles que conforman los petalos son suficientes
                                                    #Ya que cada pixel es representado por figura de entre 0 a 112 pixeles
            self.mode = 1
        else:
            self.centerArea += (self.centerArea*30/100)
        #Genera la poblacion inicial
        self.GP.startPoblacionInicial(int(self.petalArea),int(self.centerArea))
        self.start()
    def stop(self):
        self.state = 0
    def start(self):
        if self.state == 1:#Si no esta pausado
            self.view.root.title("Generacion "+str(self.GP.genCounter))
            individualList = [self.GP.getPoblacionPetalo(),self.GP.getPoblacionCentro()]
            #Llamo a drawFlower para pintar la flor con la poblacion del centro y del petalo
            self.drawFlower(individualList)
            #self.GP.avanzarGenContinua() #Avanza de 5 gen en 5 gen
            self.GP.avanzarGeneracion()
            #Si es la primera generacion guarda la flor pintada(flor original) en un panel original
            if self.GP.genCounter == 1:
                imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
                self.view.OGimagePanel.configure(image = imgtk)
                self.view.OGimagePanel.image = imgtk
            self.view.imagePanel.after(1000,self.start)
    def restart(self):
        self.state = 1
        self.start()
    #PARA FORMAR LA FLOR
    #Obtiene los puntos de los lados que conforman el rectangulo que encierra al petalo
    def getLimits(self):
        #Puntos del rectangulo que encierra a la flor
        #o ancho y largo
        originalLimits = [[-1,-1],[-1,-1],[-1,-1],[-1,-1]] #arriba,abajo,izq,der
        for dot in self.promShape:
            x = dot[0]
            y = dot[1]
            #Se busca la yMenor la cual sera la y del punto del lado horizontal de arriba
            if(y < originalLimits[0][1] or originalLimits[0][1] == -1):
                originalLimits[0] = [x,y]
            #Se busca la yMayor la cual sera la y del punto del lado horizontal de abajo
            if(y > originalLimits[1][1] or originalLimits[1][1] == -1):
                originalLimits[1] = [x,y]
            #Se busca la xMenor la cual sera la x del punto del lado izquierdo
            if(x < originalLimits[2][0] or originalLimits[2][0] == -1 ):
                originalLimits[2] = [x,y]
            #Se busca la xMayor la cul sera la x del punto del lado derecho
            if(x > originalLimits[3][0] or originalLimits[3][0] == -1):
                originalLimits[3] = [x,y]
        return originalLimits
    #Obtiene los puntos de nuestro petalo
    def buildPetal(self):
        originalPetal = []
        for newDot in range(int(self.petalArea)):#Por cada pixel dentro del area del petalo
            #Genera una x random entre los limites que consigio antes, es decir entre las x de los limites de los lados derecha e izq
            x = random.randint(self.originalLimits[2][0],self.originalLimits[3][0])
            #Genera una y random entre los limites que consigio antes, es decir entre las y de los limites de los lados arriba y abajo
            y = random.randint(self.originalLimits[0][1],self.originalLimits[1][1])
            #El punto que genere puede estar dentro del rectangulo mas no dentro del petalo entonces verificamos eso 
            while cv2.pointPolygonTest(self.contour,(x,y),False)<0:    
                x = random.randint(self.originalLimits[2][0],self.originalLimits[3][0])
                y = random.randint(self.originalLimits[0][1],self.originalLimits[1][1])
            originalPetal.append([x,y])#Guardamos el punto
        #Retornamos al final todos los puntos que pertenecen al petalo
        return originalPetal
    def buildCenter(self):
        center = []
        promRadio = self.getPromRadio()
        for newDot in range(int(self.centerArea)):
            #Genero x y y randoms dentro de un cuadrado que me encierra el centro del circulo
            x = random.randint(int(self.centroProm[0]-promRadio),int(self.centroProm[0]+promRadio))
            y = random.randint(int(self.centroProm[1]-promRadio),int(self.centroProm[1]+promRadio))
            distBetDot_Cen = math.sqrt(((x-self.centroProm[0])**2)+((y-self.centroProm[1])**2))#Distancia entre punto y centro 
            #Si la distancia es mayor al radio entonces el punto no esta dentro del circulo
            while distBetDot_Cen > promRadio:    
                x = random.randint(int(self.centroProm[0]-promRadio),int(self.centroProm[0]+promRadio))
                y = random.randint(int(self.centroProm[1]-promRadio),int(self.centroProm[1]+promRadio))
                distBetDot_Cen = math.sqrt(((x-self.centroProm[0])**2)+((y-self.centroProm[1])**2))
            center.append([x,y])
        return center
    def drawFlower(self,individualList):
        self.img = np.zeros( (550,550,3),np.uint8) 
        petalIndividual = individualList[0]
        centerIndividual = individualList[1]
        #PINTA PETALOS
        angle = 360/self.quantPetals#Angulo para rotar el petalo
        originalPetal = self.buildPetal()#Petalo original
        #Recorro la cantidad de petalos
        for petaloId in range(self.quantPetals):
            #Roto el petalo original
            petal = self.rotateShape(originalPetal,math.radians(angle)*petaloId,self.centroProm)
            #Por cada punto en el petalo
            for dot in petal:
                #Obtengo el color de un individuo random
                color = (self.GP.findColorOfIndividual(petalIndividual[random.randint(0,len(petalIndividual)-1)][0].getCromosoma(),self.GP.petalColorsTable))
                #Establece como pintar dependiendo del modo
                if self.mode == 0:
                    self.img[dot[0],dot[1]] = color#Pinta el pixel
                else:
                    #Crea una figura en base al punto 
                    rango = self.RANGO_DIMENSION_PINTAR
                    contours = np.asarray([[dot[0],dot[1]-random.randint(-rango,rango)],[dot[0]-random.randint(-rango,rango),dot[1]],[dot[0],dot[1]+random.randint(-rango,rango)],[dot[0]+random.randint(-rango,rango),dot[1]]], 'int32')
                    cv2.fillConvexPoly(self.img, contours, (int(color[0]),int(color[1]),int(color[2])),lineType=4)
        #PINTA CENTRO
        center = self.buildCenter()
        for dot in center:
            #Obtengo el color de un individuo random
            color = (self.GP.findColorOfIndividual(centerIndividual[random.randint(0,len(centerIndividual)-1)][0].getCromosoma(),self.GP.centerColorsTable))
            #Establece como pintar dependiendo del modo
            if self.mode == 0:
                self.img[dot[0],dot[1]] = color#Pinta el pixel del color
            else:
                #Crea un circulo en base al punto
                rango = self.RANGO_RADIO_PINTAR
                cv2.circle(self.img,(dot[0],dot[1]), random.randint(0,rango), (int(color[0]),int(color[1]),int(color[2])),-1)
        #Actualiza la imagen
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.img))
        self.view.imagePanel.configure(image = imgtk)
        self.view.imagePanel.image = imgtk
    #Rotar recibe una lista de puntos, el angulo y el origen
    def rotateShape(self,dots,angle,origin):
        newShape = []
        ox = origin[0]
        oy = origin[1]
        for dot in dots:
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
                if flower == len(self.flowers)-1:#Si es la ultima entonces suma y divide de una vez
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
        return (prom/len(self.flowers))
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