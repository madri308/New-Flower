from IConstant import IConstant
import random

class GeneticOperator(IConstant):
    def __init__(self):
        self.size=0

    def modifyBit(self, gen,  posicion,  newBit):
        return (gen & ~(1<<(self.cantidadBits-posicion))) | (newBit<<(self.cantidadBits-posicion))

    def cross(self,gen1,gen2):
        punto = random.randint(5,self.cantidadBits-5) #Se elige un punto para hacer el intercambio

        gen1 = gen1 >> (self.cantidadBits-punto)
        gen1 = gen1 << (self.cantidadBits-punto)

        gen2 = gen2 & (2**(self.cantidadBits-punto) - 1)

        return gen1 ^ gen2

    def mutate(self,newGen):
        if (random.random() <= 0.075):
            punto = random.randint(1,self.cantidadBits)
            bitNumber = newGen & (1 << (self.cantidadBits-punto))
            bitNumber = bitNumber >> (self.cantidadBits-punto)
            if bitNumber == 0:
                return modifyBit(newGen,punto,1)
            return modifyBit(newGen,punto,0)
        else:
            return newGen
    

