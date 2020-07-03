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
        self.poblacion = []
        self.cruzador = GeneticOperator()

    def getPoblacion(self):
        return self.poblacion
    
    ## 1. Poblacion inicial
    def startPoblacionInicial(self):
        for individuo in range(self.cantidadIndividuos):
            self.poblacion.append([Individuo(random.randint(0,self.bits-1)),0]) # de la interfaz


    ## Encontrar en la tabla el color del Individuo, retorna una lista
    def findColorOfIndividual(self,colorId):
        for colorRange in range(len(self.petalColorsTable)):
            if (colorId >= self.petalColorsTable[colorRange][3] and colorId <= self.petalColorsTable[colorRange][4]):
                return self.petalColorsTable[colorRange][0]

    ## Saca la luminosidad con la fórmula
    def getLuminosidad(self,rgb):
        return (0.299*rgb[0]**2 + 0.587*rgb[1]**2 + 0.114*rgb[2]**2)**0.5

    ## Saca el Optimo rango de un espectro R, G o B
    def getMin_Max(self,color,rango):
        optimo = rango * ((color//rango) + 1)
        if (optimo/255 > 1):
            return 255
        return optimo

    def getColorOptimo(self,colorRGB):
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

        for rangeValue in range(len(orden)):
            multiplo = 0
            if (orden[rangeValue] == 1):
                multiplo = self.rango[0]
            elif(orden[rangeValue] == 0):
                multiplo = self.rango[1]
            else:
                multiplo = self.rango[2]
            optimoColor = self.getMin_Max(colorRGB[rangeValue],multiplo)
            optimo.append(optimoColor)
        return optimo

    ## pasa el fitness a todos
    def fitness(self):
        index = 0
        for indivNumero in range (len(self.poblacion)):
            colorIndividuo = self.findColorOfIndividual(self.poblacion[indivNumero][0].getCromosoma())
            calificacion = self.getLuminosidad(colorIndividuo) / self.getLuminosidad(self.getColorOptimo(colorIndividuo))
            self.poblacion[indivNumero][1] = calificacion


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

    def Sort(self,sub_li): 
        sub_li.sort(key = lambda x: x[1], reverse = True) 
        return sub_li 

    def showPoblacion(self):
        print("Población actual -> Size: " + str(len(self.poblacion)))
        for index in range (len(self.poblacion)):
            individuo = self.poblacion[index][0]
            print ("Individuo = " + str(individuo.getCromosoma()) + " " + str(self.findColorOfIndividual(individuo.getCromosoma())))
        print()

    def avanzarGeneracion(self):
        ## 2. Aplicar fitness
        self.fitness()

        self.poblacion = self.Sort(self.poblacion)

        ## 3. Cruces y mutacion
        ##Las veces que va a agarrar una pareja
        ##
        cantidadParejas = ((len(self.poblacion) * self.individuosTomados) // 100) // 2 
        for i in range (cantidadParejas):
            individuo1 = self.poblacion[i][0]
            individuo2 = self.poblacion[i+1][0]
            cromosoma = self.cruzador.cross(individuo1.getCromosoma(),individuo2.getCromosoma())
            cromosoma = self.cruzador.mutate(cromosoma)
            self.poblacion.append([Individuo(cromosoma),0])
        
        #self.showPoblacion()            

    ## Va a reproducir a la población tantas veces como generaciones se desean
    def avanzarGenContinua(self):
        ## 1. Iniciar Poblacion
        self.startPoblacionInicial()
        self.showPoblacion() 
        for numGen in range (self.generacionMax):
            self.avanzarGeneracion()

        #self.showPoblacion() 


#alg = GeneticProcessor()
#alg.startPoblacionInicial()
#for x in alg.getPoblacion():
#    print(x.cromosoma)
