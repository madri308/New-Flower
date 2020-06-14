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
    def __init__(self,color,tamanno):
        self.color = color
        self.tamanno = tamanno
        self.pixeles = []

    def addPixel(self,pixel):
        pixeles.append(pixel)

class Centro:
    def __init__(self,diameter,color):
        self.diameter = diameter
        self.color = color
        self.pixeles = []

    def addPixel(self,pixel):
        pixeles.append(pixel)




#flor = Flor()
#pixel = Pixel(123,12,123,25,100)
#flor.addToHash('123-25-100-123-12',pixel)
#print ("hash['123-25-100-123-12']: ")
#flor.pixeles['123-25-100-123-12'].print_pixel()