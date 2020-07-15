from dataAnalyzer import *
class Flor:
    def __init__(self,image,dots,imageID,uniqueColors):
        self.uniqueColors = uniqueColors
        self.ID = imageID
        self.image = image
        #FLOR TIENE SU ANALIZADOR QUE NOS VA A DAR DATOS EN BASE A LO QUE NOS DIO EL USUARIO 
        self.analyzer = DataAnalyzer(image=self.image,
                                     dots=dots,
                                     imageID=self.ID,
                                     uniqueColors = self.uniqueColors)   
        #VORAZ PARA CONSEGUIR LOS PIXELES LIMPIOS POR DECIRLO ASI 
        self.pixeles = self.analyzer.getPixelsImageCleaned()  
        #CENTRO DE LA FLOR Y SUS CARACTERISTICAS
        self.addCentro(radio = self.analyzer.getCenterRadio(),
                        area = self.analyzer.getCenterArea(),
                        color = self.analyzer.getCenterPrincipalColor(),
                        pixeles = self.analyzer.getCenterPixels())
        #PETALO DE LA FLOR Y SUS CARACTERISTICAS
        self.addPetalo(area = self.analyzer.getCenterArea(),
                        contorno = self.analyzer.getPetalShapeDots(),
                        color = self.analyzer.getPetalPrincipalColor(),
                        pixeles = self.analyzer.getPetalPixels())
        self.cantPetalos = self.analyzer.getQuantityOfPetals()#Cantidad de petalos
        self.centroPuntos = self.analyzer.getTotalCenter()#Punto central de la flor
        
    def addCentro(self,radio,area,color,pixeles):
        self.centro = Centro(area,radio,color,pixeles)

    def addPetalo(self,color,area,contorno,pixeles):
        self.petalo = Petalo(color,area,contorno,pixeles)
class Petalo:
    def __init__(self,color,area,contorno,pixeles):
        self.color = color
        self.area = area
        self.contorno = contorno
        self.pixeles = pixeles

class Centro:
    def __init__(self,area,radio,color,pixeles):
        self.area = area
        self.radio = radio
        self.color = color
        self.pixeles = pixeles

#flor = Flor()
#pixel = Pixel(123,12,123,25,100)
#flor.addToHash('123-25-100-123-12',pixel)
#print ("hash['123-25-100-123-12']: ")
#flor.pixeles['123-25-100-123-12'].print_pixel()