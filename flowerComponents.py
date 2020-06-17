from dataAnalyzer import *
class Flor:
    def __init__(self,image,dots,imageID):
        self.ID = imageID
        self.image = image
        self.analyzer = DataAnalyzer(image=self.image,
                                     dots=dots,
                                     imageID=self.ID)     
        self.pixeles = {}
        self.addCentro(radio = self.analyzer.getCenterRadio(),
                        area = self.analyzer.getCenterArea(),
                        color = self.analyzer.getCenterPrincipalColor())
        self.addPetalo(area = self.analyzer.getCenterArea(),
                        contorno = self.analyzer.getPetalShapeDots(),
                        color = self.analyzer.getPetalPrincipalColor())

    def addCentro(self,radio,area,color):
        print(color)
        self.centro = Centro(area,radio,color)

    def addPetalo(self,color,area,contorno):
        print(contorno)
        self.petalos = Petalo(color,area,contorno)

    def addToHash(self,key,value):
        self.pixeles[key] = value

    #retorna un objeto Pixel
    def getValueOfHash(self,key):
        return self.pixeles[key]

class Pixel:
    def __init__(self,x,y,r,g,b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
    
    def print_pixel(self):
        print("x: " + str(self.x))
        print("y: " + str(self.y))
        print("r: " + str(self.r))
        print("g: " + str(self.g))
        print("b: " + str(self.b))

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