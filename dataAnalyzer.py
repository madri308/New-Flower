import numpy as np
import math

class DataAnalyzer:
    def __init__(self,image,dots,imageID):
        self.image = image
        self.dots = dots
        self.imageID = imageID
    def getPetalShapeDots(self):
        totalDots = []
        for dot in range (5,len(self.dots)):
            totalDots.append(self.dots[dot])
        return totalDots
    def getPetalArea(self):
        area = 0.0
        n = len(self.dots)-5
        j = n - 1
        for i in range(0,n): 
            area += (self.dots[j+5][1] + self.dots[i+5][1]) * (self.dots[j+5][2] - self.dots[i+5][2]) 
            j = i  
        petalArea = (int(abs(area / 2.0))) 
        return petalArea
    def getCenterRadio(self):
        radio = math.sqrt(((self.dots[2][1]-self.dots[3][1])**2)+((self.dots[2][2]-self.dots[3][2])**2))
        return radio
    def getCenterArea(self):
        radio = self.getCenterRadio()
        centerArea = math.pi*radio*radio
        return centerArea
    def getCenterPrincipalColor(self):
        color = self.dots[1][0]
        return color
    def getPetalPrincipalColor(self):
        color = self.dots[0][0]
        return color

    




