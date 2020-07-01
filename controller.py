from flowerComponents import *
from geneticOperator import *
from geneticProcessor import *
class Controller:
    flowers = []
    allPixels = []
    GP = GeneticProcessor()
    def __init__(self, flowers):
        for i in range(len(flowers)):
            self.flowers.append(flowers[i])   
            self.allPixels = self.allPixels+flowers[i].pixeles

        ## Comienza el GA --------------------
        self.GP.createTable(self.allPixels)
        #print()
        #self.GP.showTable()
        #print()
        self.GP.avanzarGenContinua()

    def resultsView(self):
        pass