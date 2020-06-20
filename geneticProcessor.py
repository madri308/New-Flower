from geneticOperator import GeneticOperator
from IConstant import IConstant
import random


class Individuo:
    def __init__(self,valorCromosoma):
        self.cromosoma = valorCromosoma
    
    def getCromosoma(self):
        return self.cromosoma


class GeneticProcessor(IConstant):
    def __init__(self):
        self.individuos = []
        self.cruzador = GeneticOperator()

    def getIndividuos(self):
        return self.individuos
    
    ## 1. Poblacion inicial
    def startPoblacionInicial(self):
        for individuo in range(self.cantidadIndividuos):
            self.individuos.append(Individuo(random.randint(0,self.bits-1))) # de la interfaz
    
    def fitness(self):
        pass
    


#alg = GeneticProcessor()
#alg.startPoblacionInicial()
#for x in alg.getIndividuos():
#    print(x.cromosoma)