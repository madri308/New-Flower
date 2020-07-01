from geneticOperator import GeneticOperator
from IConstant import IConstant
import random
from dataAnalyzer import *

class Individuo:
    def __init__(self,valorCromosoma):
        self.cromosoma = valorCromosoma
    
    def getCromosoma(self):
        return self.cromosoma

class GeneticProcessor(IConstant):
    table = []
    def __init__(self):
        self.poblacion = []
        self.cruzador = GeneticOperator()

    def getPoblacion(self):
        return self.poblacion
    
    ## 1. Poblacion inicial
    def startPoblacionInicial(self):
        for individuo in range(self.cantidadIndividuos):
            self.poblacion.append(Individuo(random.randint(0,self.bits-1))) # de la interfaz
    
    def fitness(self):
        pass
    def createTable(self,pixels):
        total = len(pixels)
        for pixel in range(len(pixels)):
            pixelColor = pixels[pixel].color
            encontrado = False
            for color in range(len(self.table)):
                if (pixelColor[0]+pixelColor[1]+pixelColor[2]) - (self.table[color][0][0]+self.table[color][0][1]+self.table[color][0][2]) == 0:
                     self.table[color][1] += 1
                     apariciones = self.table[color][1]
                     porcentaje = apariciones*100/total
                     self.table[color][2] = porcentaje
                     encontrado = True

            if encontrado == False:
                        #color,aparicion,porcentaje
                color = [pixelColor,1,100/total]
                self.table.append(color)
            
        maxAnterior = 0
        for color in range(len(self.table)):
            self.table[color].append(maxAnterior)
            max1 = self.bits*self.table[color][2]/100
            self.table[color].append(maxAnterior+max1-1)
            maxAnterior = maxAnterior+max1
    def showTable(self):
        for color in range(len(self.table)):
            print(self.table[color][0]," ",self.table[color][1]," ",self.table[color][2]," ",self.table[color][3]," ",self.table[color][4])

    


#alg = GeneticProcessor()
#alg.startPoblacionInicial()
#for x in alg.getPoblacion():
#    print(x.cromosoma)
