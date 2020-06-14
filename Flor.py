from dataAnalyzer import *
class Flor:
    def __init__(self,image,dots,imageID):
        self.ID = imageID
        self.image = image
        self.analyzer = DataAnalyzer(image=self.image,dots=dots,imageID=self.ID)
        
        self.cantidadPetalos = 0
        self.petalos = []
        self.pixeles = {}

    def addCentro(self,diameter,color):
        self.centro = Centro(diameter,color)

    def addPetalos(self,color,tamanno):
        self.petalos.append(Petalo(color,tamanno))

    def setCantidadPetalos(self,cantidad):
        self.cantidadPetalos = cantidad

    def addToHash(self,key,value):
        self.pixeles[key] = value

    #retorna un objeto Pixel
    def getValueOfHash(self,key):
        return self.pixeles[key]