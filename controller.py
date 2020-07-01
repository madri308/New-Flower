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
        self.GP.createTable(self.allPixels)
    def resultsView(self):
        