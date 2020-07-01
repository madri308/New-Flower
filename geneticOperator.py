from IConstant import IConstant
import random

class GeneticOperator(IConstant):
    def __init__(self):
        self.size=0

    def convertBin(self,numero):
        numero = bin(numero)[2:]
        completado = ''
        for x in range(self.cantidadBits-len(numero)):
            completado += '0'
        return completado + numero

    def cross(self,gen1,gen2):
        punto = random.randint(5,self.cantidadBits-5) #Se elige un punto para hacer el intercambio
        newIndividuo = ''
        gen1 = self.convertBin(gen1)
        gen2 = self.convertBin(gen2)
        newIndividuo = gen1[:punto] + gen2[punto:] #Se mezcla el material genetico de los padres en cada nuevo individuo
        return int(newIndividuo,2)

    def mutate(self,newGen):
        if (random.random() <= 0.075):
            punto = random.randint(0,self.cantidadBits-1)
            #print(punto)
            gen = self.convertBin(newGen)
            if (gen[punto] == '0'):
                gen = gen[:punto] + '1' + gen[punto+1:] 
            else:
                gen = gen[:punto] + '0' + gen[punto+1:]
            return int(gen,2)
        else:
            return newGen
    

