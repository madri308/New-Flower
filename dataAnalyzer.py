from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
#np.seterr(over='ignore')
import math

class DataAnalyzer:
    pixelsCenter = []#Pixeles del centro que se obtienen del voraz
    pixelsPetal = []#Pixeles del petalo que se obtienen del voraz
    def __init__(self,image,dots,imageID,uniqueColors):
        self.uniqueColors = uniqueColors
        self.image = image
        self.dots = dots
        self.imageID = imageID
        self.allPixels = np.array(image)
    #CONTORNOS
    def getPetalShapeDots(self):
        totalDots = []
        for dot in range (5,len(self.dots)):#Empieza desde la pos 5 en adelante porque ahi estan los puntos del contorno
            totalDots.append(self.dots[dot])
        return totalDots
    #AREAS.
    def getPetalArea(self):
        area = 0.0
        cantPuntos = len(self.dots)-5#todos los puntos menos 5 que corresponden a otra informacion
        puntoRelac = cantPuntos - 1#Ultimo punto en este caso
        for punto in range(0,cantPuntos): 
            #Es el punto +5 porque ahi empiezan los puntos de contorno
            #           X puntoRelacionado           X puntoActual           Y puntoRelacionado            Y puntoActual
            area += (self.dots[puntoRelac+5][1] + self.dots[punto+5][1]) * (self.dots[puntoRelac+5][2] - self.dots[punto+5][2]) 
            puntoRelac = punto #punto relacionado sera el actual y el actual se debe actualizar a el que sigue
        petalArea = (int(abs(area / 2.0))) 
        return petalArea
    def getCenterArea(self):
        radio = self.getCenterRadio()
        centerArea = math.pi*radio*radio
        return centerArea
    def getTotalArea(self):
        radio = self.getTotalFlowerRadio()
        totalArea = math.pi*radio*radio
        return totalArea
    #DIMENSIONES
    def getTotalCenter(self):
        return self.dots[2]
    def getCenterRadio(self):
        radio = math.sqrt(((self.dots[2][1]-self.dots[3][1])**2)+((self.dots[2][2]-self.dots[3][2])**2))
        return radio
    def getTotalFlowerRadio(self):
        radio = math.sqrt(((self.dots[2][1]-self.dots[4][1])**2)+((self.dots[2][2]-self.dots[4][2])**2))
        return radio
    #COLORES
    def getCenterPrincipalColor(self):
        color = self.dots[1][0]#es donde esta el color principal del centro escogido por el user en la lista
        return color
    def getPetalPrincipalColor(self):
        color = self.dots[0][0]#es donde esta el color principal del petalo escogido por el user en la lista
        return color
    #PIXELES
    def getPixelsImageCleaned(self):        
        #Guarda los colors optimos, los que mi voraz va usar como referencia
        centerPrincipalColor = self.getCenterPrincipalColor()
        petalPrincipalColor = self.getPetalPrincipalColor()

        altura =len(self.allPixels)
        ancho = len(self.allPixels[0])
        tipoPixel = ""
        #RECORRO FILAS Y COLUMNAS PARA IR EVALUANDO PIXELES
        for pixely in range(altura):
            for pixelx in range(ancho):
                pixelColor = self.allPixels[pixely][pixelx]#Color del pixel actual
                diffBetCenC_PxlC = self.getColorDistance(pixelColor,centerPrincipalColor)#Diferencia entre color actual y color optimo del centro
                diffBetPetC_PxlC = self.getColorDistance(pixelColor,petalPrincipalColor)#Diferencia entre color actual y color optimo del petalo
                
                tipoPixel = ""
                center = self.getTotalCenter()
                dBetC_P = math.sqrt(((pixelx-center[1])**2)+((pixely-center[2])**2))#Distancia entre el centro y el pixel actual
                #Si la dif entre colorCentroOptimo y colorPixel es menor a la cant de pixeles de la imagen entre la cant de colores total de la imagen
                #y la distancia entre el pixel y el centro es menor al radio del centro (es decir esta dentro del centro)
                if diffBetCenC_PxlC < altura*ancho/self.uniqueColors and dBetC_P < self.getCenterRadio() :#COMO NO ALAMBRAR ESTO?? totalpixels/cantidad de colores
                    #Entonces crea un pixel y lo guarda en la lista de los pixeles del centro limpios
                    tipoPixel = "C"
                    pixel = Pixel(x = pixelx, y = pixely, color = self.allPixels[pixely][pixelx], type = tipoPixel)
                    self.pixelsCenter.append(pixel)
                #Si la dif entre colorPetaloOptimo y colorPixel es menor a la cant de pixeles de la imagen entre la cant de colores total de la imagen
                #y la distancia entre el pixel y el centro es menor al radio total de la flor (es decir esta dentro de la flor)
                elif diffBetPetC_PxlC < altura*ancho/self.uniqueColors and dBetC_P < self.getTotalFlowerRadio():
                    #Entonces crea un pixel y lo guarda en la lista de los pixeles del petalo limpios
                    tipoPixel = "P"
                    pixel = Pixel(x = pixelx, y = pixely, color = self.allPixels[pixely][pixelx], type = tipoPixel)
                    self.pixelsPetal.append(pixel)
        return self.pixelsPetal+self.pixelsCenter#Retorna todos los pixeles en total
    def getPetalPixels(self):
        return self.pixelsPetal
    def getCenterPixels(self):
        return self.pixelsCenter
    def getColorDistance(self,RGB1,RGB2):
        rmean = ((RGB1[0]) + (RGB2[0])-2)
        r = ((RGB1[0] - (RGB2[0])))
        g = ((RGB1[1] - (RGB2[1])))
        b = ((RGB1[2] - (RGB2[2])))
        difference = math.sqrt((((512+rmean)*r*r)>>8)+ 4*g*g + (((767-rmean)*b*b)>>8))
        return difference
    #CANTIDADES
    def getQuantityOfPetals(self):
        #Agarramos el total del area correspondiente a petalos(areaTotal-areaCentro) y la dividimos entre el areaPetalo
        return int((self.getTotalArea()-self.getCenterArea())/self.getPetalArea())
class Pixel:
    def __init__(self,x,y,color,type):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
    
    def print_pixel(self):
        print("x: " + str(self.x))
        print("y: " + str(self.y))
        print("color: " + str(self.color))
        print("tipo: " + str(self.type))
    




