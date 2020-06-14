import numpy as np

class dataAnalyzer:

    def __init__(self,image,dots,imageID):
        self.image = image
        self.dots = dots
        self.imageID = imageID
        self.petalArea(self.dots)
    def petalArea(self,dots):
        area = 0.0
        n = len(dots)-5
        j = n - 1
        for i in range(0,n): 
            area += (dots[j+5][1] + dots[i+5][1]) * (dots[j+5][2] - dots[i+5][2]) 
            j = i  
        print(int(abs(area / 2.0)) ) 


