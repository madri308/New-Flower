from dataAnalyzer import *
class Flor:
    def __init__(self,image,dots,imageID,uniqueColors):
        self.uniqueColors = uniqueColors
        self.ID = imageID
        self.image = image
        self.analyzer = DataAnalyzer(image=self.image,
                                     dots=dots,
                                     imageID=self.ID)     
        self.addCentro(radio = self.analyzer.getCenterRadio(),
                        area = self.analyzer.getCenterArea(),
                        color = self.analyzer.getCenterPrincipalColor())
        self.addPetalo(area = self.analyzer.getCenterArea(),
                        contorno = self.analyzer.getPetalShapeDots(),
                        color = self.analyzer.getPetalPrincipalColor())
        self.pixeles = self.analyzer.getPixelsImageCleaned(self.uniqueColors)
        for pixel in range(len(self.pixeles)):
             self.pixeles[pixel].print_pixel()
        
    def addCentro(self,radio,area,color):
        self.centro = Centro(area,radio,color)

    def addPetalo(self,color,area,contorno):
        self.petalos = Petalo(color,area,contorno)

    def addToHash(self,key,value):
        self.pixeles[key] = value

    #retorna un objeto Pixel
    def getValueOfHash(self,key):
        return self.pixeles[key]
class Petalo:
    def __init__(self,color,area,contorno):
        self.color = color
        self.area = area
        self.contorno = contorno
        self.pixeles = []

    def addPixel(self,pixel):
        self.pixeles.append(pixel)

class Centro:
    def __init__(self,area,radio,color):
        self.area = area
        self.radio = radio
        self.color = color
        self.pixeles = []

    def addPixel(self,pixel):
        self.pixeles.append(pixel)

#flor = Flor()
#pixel = Pixel(123,12,123,25,100)
#flor.addToHash('123-25-100-123-12',pixel)
#print ("hash['123-25-100-123-12']: ")
#flor.pixeles['123-25-100-123-12'].print_pixel()