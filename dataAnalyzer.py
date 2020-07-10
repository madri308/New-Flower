from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
#np.seterr(over='ignore')
import math

class DataAnalyzer:
    pixelsCenter = []
    pixelsPetal = []
    def __init__(self,image,dots,imageID,uniqueColors):
        self.uniqueColors = uniqueColors
        self.image = image
        self.dots = dots
        self.imageID = imageID
        self.allPixels = np.array(image)
    #CONTORNOS
    def getPetalShapeDots(self):
        totalDots = []
        for dot in range (5,len(self.dots)):
            totalDots.append(self.dots[dot])
        return totalDots
    #AREAS.
    def getPetalArea(self):
        area = 0.0
        n = len(self.dots)-5
        j = n - 1
        for i in range(0,n): 
            area += (self.dots[j+5][1] + self.dots[i+5][1]) * (self.dots[j+5][2] - self.dots[i+5][2]) 
            j = i  
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
        color = self.dots[1][0]
        return color
    def getPetalPrincipalColor(self):
        color = self.dots[0][0]
        return color
    #PIXELES
    def getPixelsImageCleaned(self):        
        centerPrincipalColor = self.getCenterPrincipalColor()
        petalPrincipalColor = self.getPetalPrincipalColor()

        altura =len(self.allPixels)
        ancho = len(self.allPixels[0])
        tipoPixel = ""
      
        for pixely in range(altura):
            for pixelx in range(ancho):
                pixelColor = self.allPixels[pixely][pixelx]
                diffBetCenC_PxlC = self.getColorDistance(pixelColor,centerPrincipalColor)
                diffBetPetC_PxlC = self.getColorDistance(pixelColor,petalPrincipalColor)
                
                tipoPixel = ""
                center = self.getTotalCenter()
                dBetC_P = math.sqrt(((pixelx-center[1])**2)+((pixely-center[2])**2))
                if diffBetCenC_PxlC < altura*ancho/self.uniqueColors and dBetC_P < self.getCenterRadio() :#COMO NO ALAMBRAR ESTO?? totalpixels/cantidad de colores
                    tipoPixel = "C"
                    pixel = Pixel(x = pixelx, y = pixely, color = self.allPixels[pixely][pixelx], type = tipoPixel)
                    self.pixelsCenter.append(pixel)
                elif diffBetPetC_PxlC < altura*ancho/self.uniqueColors and dBetC_P < self.getTotalFlowerRadio():
                    tipoPixel = "P"
                    pixel = Pixel(x = pixelx, y = pixely, color = self.allPixels[pixely][pixelx], type = tipoPixel)
                    self.pixelsPetal.append(pixel)
        return self.pixelsPetal+self.pixelsCenter
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
    




