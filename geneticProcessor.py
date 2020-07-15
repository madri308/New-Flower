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
    petalColorsTable = []
    centerColorsTable = []
    def __init__(self):
        self.poblacionPetalo = []
        self.poblacionCentro = []
        self.cruzador = GeneticOperator()
        self.genCounter = 0

    def getPoblacionPetalo(self):
        return self.poblacionPetalo
    
    def getPoblacionCentro(self):
        return self.poblacionCentro
    
    ## 1. Poblacion inicial
    def startPoblacionInicial(self,cantidadIndividuosPetalo,cantidadIndividuosCentro):
        for individuo in range(cantidadIndividuosPetalo):
            self.poblacionPetalo.append([Individuo(random.randint(0,self.BITS-1)),0]) # de la interfaz
        for individuo in range(cantidadIndividuosCentro):
            self.poblacionCentro.append([Individuo(random.randint(0,self.BITS-1)),0])

        print("Numero de poblacion Centro: " + str(len(self.poblacionCentro)))
        print("Numero de poblacion Pétalo: " + str(len(self.poblacionPetalo)))

    ## Encontrar en la tabla el color del Individuo, retorna una lista
    def findColorOfIndividual(self,colorId,tabla):
        for colorRange in range(len(tabla)):
            if (colorId >= tabla[colorRange][3] and colorId <= tabla[colorRange][4]):
                return tabla[colorRange][0]
        
        ## Pasa pocas veces, devuelve el ultimo color de la lista grande
        return tabla[len(tabla)-1][0] #-- PROBLEMA RESUELTO, PUEDE HABER COLORES QUE LLEGUEN A ESPECTROS MAYORES AL RANGO
        

    ## Saca la luminosidad con la fórmula
    def getLuminosidad(self,rgb):
        return (0.299*rgb[0]**2 + 0.587*rgb[1]**2 + 0.114*rgb[2]**2)**0.5

    ## Saca el Optimo rango de un espectro R, G o B
    def getMin_Max(self,color,rango):
        optimo = rango * ((color//rango) + 1)
        if (optimo/255 > 1):
            return 255
        return optimo

    ## 
    def getColorOptimo(self,colorRGB):
        ## Se asignan del R,G y B el mayor, menor y medio con los valores 1, -1 y 0 respectivamente
        orden = [0,0,0]
        optimo = []
        if (colorRGB[0] >= colorRGB[1] and colorRGB[0] >= colorRGB[2]):
            orden[0] = 1
            if (colorRGB[1] >= colorRGB[2]):
                orden[2] = -1
            else:
                orden[1] = -1
        elif (colorRGB[1] >= colorRGB[0] and colorRGB[1] >= colorRGB[2]):
            orden[1] = 1
            if (colorRGB[0] >= colorRGB[2]):
                orden[2] = -1
            else:
                orden[0] = -1
        elif (colorRGB[2] >= colorRGB[0] and colorRGB[2] >= colorRGB[1]):
            orden[2] = 1
            if (colorRGB[0] >= colorRGB[1]):
                orden[1] = -1
            else:
                orden[0] = -1
        else:
            pass

        ## Se asignan los valores con los que se mueven los colores optimos [50,25,5]
        for rangeValue in range(len(orden)):
            multiplo = 0
            if (orden[rangeValue] == 1):
                multiplo = self.RANGO[0]
            elif(orden[rangeValue] == 0):
                multiplo = self.RANGO[1]
            else:
                multiplo = self.RANGO[2]
            optimoColor = self.getMin_Max(colorRGB[rangeValue],multiplo)
            optimo.append(optimoColor)
        return optimo

    ## pasa el fitness a todos
    def fitness(self,poblacion,tabla):
        index = 0
        for indivNumero in range (len(poblacion)):
            ## Encuentra el color del individuo
            colorIndividuo = self.findColorOfIndividual(poblacion[indivNumero][0].getCromosoma(),tabla)
            
            # calificacion = luminosidad(color actual) / luminosidad(color optimo)
            calificacion = self.getLuminosidad(colorIndividuo) / self.getLuminosidad(self.getColorOptimo(colorIndividuo))
            poblacion[indivNumero][1] = calificacion
        return poblacion


    def createTable(self,pixels):
        allColors = []
        for typePixel in pixels:
            colors = []
            total = len(typePixel)
            for pixel in range(len(typePixel)):
                pixelColor = typePixel[pixel].color
                encontrado = False
                for color in range(len(colors)):
                    if (pixelColor[0]+pixelColor[1]+pixelColor[2]) - (colors[color][0][0]+colors[color][0][1]+colors[color][0][2]) == 0:
                        colors[color][1] += 1
                        apariciones = colors[color][1]
                        porcentaje = apariciones*100/total
                        colors[color][2] = porcentaje
                        encontrado = True
                if encontrado == False:
                            #color,aparicion,porcentaje
                    color = [pixelColor,1,100/total]
                    colors.append(color)
            maxAnterior = 0
            for color in range(len(colors)):
                colors[color].append(maxAnterior)
                max1 = self.bits*colors[color][2]/100
                colors[color].append(maxAnterior+max1-1)
                maxAnterior = maxAnterior+max1
            allColors.append(colors)
        self.centerColorsTable = allColors[0]
        self.petalColorsTable = allColors[1]
        self.showTable()
        
    def showTable(self):
        print("PETALOS:")
        for color in range(len(self.petalColorsTable)):
            print(self.petalColorsTable[color][0]," ",self.petalColorsTable[color][1]," ",self.petalColorsTable[color][2]," ",self.petalColorsTable[color][3]," ",self.petalColorsTable[color][4])
        print("CENTRO:")
        for color in range(len(self.centerColorsTable)):
            print(self.centerColorsTable[color][0]," ",self.centerColorsTable[color][1]," ",self.centerColorsTable[color][2]," ",self.centerColorsTable[color][3]," ",self.centerColorsTable[color][4])

    ## Hace sorting descendente de la poblacion de acuerdo a la calificacion. [individuo,calificacion]
    def Sort(self,sub_li): 
        sub_li.sort(key = lambda x: x[1], reverse = True) 
        return sub_li 

    def showPoblacion(self,poblacion,tabla):
        print("Población actual -> Size: " + str(len(poblacion)))
        for index in range (len(poblacion)):
            individuo = poblacion[index][0]
            print ("Individuo = " + str(individuo.getCromosoma()) + " " + str(self.findColorOfIndividual(individuo.getCromosoma(),tabla)))
        print()

    ## Elimina a individuos de la poblacion aleatoriamente
    def eliminarIndividuos(self,poblacion,cantidad):
        eliminadosCounter = 0
        while cantidad > eliminadosCounter:
            posicion = random.randint(0,len(poblacion)-1)
            poblacion.pop(posicion)
            eliminadosCounter += 1
        return poblacion
        
    ## Elimina a n individuos peor adaptados(No se usa actualmente porque elimina a los no aptos en muy pocas generaciones)
    def eliminarIndividuosNoAptos(self,poblacion,cantidad):
        if cantidad <= len(poblacion):
            return poblacion[:len(poblacion) - cantidad]
        return poblacion

    ## cantidadParejas-> saca cuantas parejas hacer y consecuentemente cuantos hijos habran
    def reproducirPoblacion(self,poblacion):
        cantidadParejas = ((len(poblacion) * self.INDIVIDUOS_TOMADOS) // 100) // 2
        for padre in range (cantidadParejas):
            individuo1 = poblacion[padre][0]
            individuo2 = poblacion[padre+1][0]
            cromosoma = self.cruzador.cross(individuo1.getCromosoma(),individuo2.getCromosoma())
            cromosoma = self.cruzador.mutate(cromosoma)
            poblacion.append([Individuo(cromosoma),0])
        
        ## Se eliminan a la poblacion despues de la reproduccion
        poblacion = self.eliminarIndividuos(poblacion, cantidadParejas)
        return poblacion

    ## Avanza a la siguiente generación
    def avanzarGeneracion(self):
        ## 2. Aplicar fitness
        self.poblacionCentro = self.fitness(self.poblacionCentro,self.centerColorsTable)
        self.poblacionPetalo = self.fitness(self.poblacionPetalo,self.petalColorsTable)

        self.poblacionCentro = self.Sort(self.poblacionCentro)
        self.poblacionPetalo = self.Sort(self.poblacionPetalo)

        ## 3. Cruces y mutacion
        ##Las veces que va a agarrar una pareja
        ##
    
        self.poblacionCentro = self.reproducirPoblacion(self.poblacionCentro)
        self.poblacionPetalo = self.reproducirPoblacion(self.poblacionPetalo)
        #self.showPoblacion()
        self.genCounter += 1

    ## Va a reproducir a la población tantas veces como generaciones se desean
    def avanzarGenContinua(self):
        #self.showPoblacion(self.poblacionCentro,self.centerColorsTable)
        #self.showPoblacion(self.poblacionPetalo,self.petalColorsTable) 
        
        ## opcion para generar n generaciones 
        for numGen in range (self.GENERACION_MAX):
            self.avanzarGeneracion()

        #self.showPoblacion(self.poblacionCentro,self.centerColorsTable)
        #self.showPoblacion(self.poblacionPetalo,self.petalColorsTable) 


#alg = GeneticProcessor()
#alg.startPoblacionInicial()
#for x in alg.getPoblacion():
#    print(x.cromosoma)
