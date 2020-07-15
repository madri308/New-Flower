from IConstant import IConstant
import random

class GeneticOperator(IConstant):
    def __init__(self):
        self.size=0

    ## 
    ## newBit= Bit nuevo con el que se quiere cambiar. 0 o 1
    ## Se le aplica una mascara en donde se pone en 0 la posicion que se desea con un 'and' en la primera operacion
    ## (num and -mask) or mask(0 o 1)  
    def modifyBit(self, gen,  posicion,  newBit):
        return (gen & ~(1<<(self.CANTIDAD_BITS-posicion))) | (newBit<<(self.CANTIDAD_BITS-posicion))


    def cross(self,gen1,gen2):
        punto = random.randint(self.LIMITE_RANGO_BITS,self.CANTIDAD_BITS-self.LIMITE_RANGO_BITS) #Se elige un punto para hacer el intercambio

        ## Se hace shr y luego shl para desaparecer los bits menos significativos
        gen1 = gen1 >> (self.CANTIDAD_BITS-punto)
        gen1 = gen1 << (self.CANTIDAD_BITS-punto)

        ## num and (mask-> 1s para obtener los bits menos significativos)
        gen2 = gen2 & (2**(self.CANTIDAD_BITS-punto) - 1)

        ## num1 xor num2 
        return gen1 ^ gen2

    def mutate(self,newGen):
        if (random.random() <= self.MUTATION_PROB):
            punto = random.randint(1,self.CANTIDAD_BITS)
            ## Busca el bit en la posicion deseada y ve si es 0 o 1
            ## num and mask(posicion deseada) -> devuelve el bit a la posicion menos significativa con shr
            bitNumber = newGen & (1 << (self.CANTIDAD_BITS-punto))
            bitNumber = bitNumber >> (self.CANTIDAD_BITS-punto)
            if bitNumber == 0:
                return self.modifyBit(newGen,punto,1)
            return self.modifyBit(newGen,punto,0)
        else:
            return newGen
    

