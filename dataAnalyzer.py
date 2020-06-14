import numpy as np
import math

class DataAnalyzer:
    petalArea = 0
    centerArea = 0
    def __init__(self,image,dots,imageID):
        self.image = image
        self.dots = dots
        self.imageID = imageID
        self.getPetalArea(self.dots)
        self.getCenterArea(self.dots)
    def getPetalArea(self,dots):
        area = 0.0
        n = len(dots)-5
        j = n - 1
        for i in range(0,n): 
            area += (dots[j+5][1] + dots[i+5][1]) * (dots[j+5][2] - dots[i+5][2]) 
            j = i  
        self.petalArea = (int(abs(area / 2.0))) 
    def getCenterArea(self,dots):
        radio = math.sqrt(((dots[2][1]-dots[3][1])**2)+((dots[2][2]-dots[3][2])**2) )
        self.centerArea = math.pi*radio*radio



