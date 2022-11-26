import matplotlib.pyplot as plt
import numpy as np
import sys
plt.rcParams['axes.facecolor'] = 'black'
tiempoPausa = 0.001
margenCiudad = 1
grafo = {}
numeroVerticesAlto = 25
numeroVerticesAncho = 25
temperatura = 1000
tasaEnfriamiento = 0.99

#Funciones hash para mapear de (x, y) a un numero y viceversa
def hashPuntoNumero(x, y, numeroVerticesAncho):
    return x * numeroVerticesAncho + y
def hashNumeroPunto(numero, largo, numeroVerticesAncho):
    return numero % numeroVerticesAncho, int(numero / numeroVerticesAncho)

#Calculo de la probabilidad de aceptacion
def probabilidadAceptacion(energy, newEnergy, temperatura):
    #Si la nueva solucion es mejor, se aceptara
    if newEnergy < energy:
        return 1.0
    #Si la nueva solucion es peor, se calcula su probabilidad de aceptacion
    return np.exp((energy - newEnergy) / temperatura)

#Funcion para divir arreglos con elementos de la forma (x, y) en 2 arreglos con las abscisas y ordenadas respectivamente
def separarPuntosDelTour(tour):
    abscisasTour = []
    ordenadasTour = []
    for ciudad in tour:
        x, y = hashNumeroPunto(ciudad, numeroVerticesAlto, numeroVerticesAncho)
        abscisasTour.append(x)
        ordenadasTour.append(y)
    return abscisasTour, ordenadasTour

def make_link(grafo, node1, node2, cost):
    if node1 not in grafo:
        grafo[node1] = {}
    (grafo[node1])[node2] = cost
    if node2 not in grafo:
        grafo[node2] = {}
    (grafo[node2])[node1] = cost
    return grafo

#Funcion para proponer una ruta para start y end en el grafo a traves de una exploracion del grafo de forma aleatoria
def crearRuta(G, start, end):
    camino = [start]
    noAccesibles = []
    ubicacionActual = start
    while ubicacionActual != end:
        #Se quiere saber si todos los vecinos al nodo actual son inaccesibles, es decir, si todos estos vecinos estan en la ruta propuesta o en la lista de nodos inaccesibles
        todosLosVecinosSonInaccesibles = True
        for vecino in G[ubicacionActual]:
            if vecino not in camino and vecino not in noAccesibles:
                todosLosVecinosSonInaccesibles = False
                break
        
        #Si se sabe que todos los vecinos al nodo actual son inaccesibles, entonces se elimina el nodo actual de la ruta, se anade el nodo actual a la lista de nodos accesibles y se considera el ultimo nodo de la ruta como nodo actual para continuar formando la ruta
        if todosLosVecinosSonInaccesibles:
            camino.remove(ubicacionActual)
            noAccesibles.append(ubicacionActual)
            ubicacionActual = camino[len(camino) - 1]
            continue

        #En caso de que haya un nodo vecino que se pueda escoger para formar la ruta se esocge al azar un nodo para agregarlo a la ruta de tal forma que no este en la ruta y no este en la lista de nodos inaccesibles y luego considerar como nodo actual al nodo que se agrego
        numero = np.random.randint(len(G[ubicacionActual]))
        temporal = 0
        nuevaUbicacion = None
        for vecino in G[ubicacionActual]:
            if temporal == numero:
                nuevaUbicacion = vecino
                break
            else:
                temporal += 1
        
        while vecino in camino or vecino in noAccesibles:
            numero = np.random.randint(len(G[ubicacionActual]))
            temporal = 0
            nuevaUbicacion = None
            for vecino in G[ubicacionActual]:
                if temporal == numero:
                    nuevaUbicacion = vecino
                    break
                else:
                    temporal += 1
        camino.append(vecino)
        ubicacionActual = nuevaUbicacion
    return camino

#Funcion para modicar la ruta propuesta donde se considera la subruta para a y c como una ruta valida y se propone una nueva ruta para c y b donde c es un nodo de la ruta propuesta tal que c != a y c != b
def crearRutaModificada(G, ruta):
    puntoCorte = np.random.randint(len(ruta) - 2)
    rutaModificada = []
    for indice in range(puntoCorte + 1):
        rutaModificada.append(ruta[indice])
    subrutaFinal = crearRuta(G, ruta[puntoCorte + 1], ruta[len(ruta) - 1])
    for nodo in subrutaFinal:
        rutaModificada.append(nodo)
    return rutaModificada

def calcularDistanciaRuta(grafo, ruta):
    distancia = 0
    for indice in range(len(ruta) - 1):
        inicio = ruta[indice]
        final = ruta[indice + 1]
        distancia += grafo[inicio][final]
    return distancia

#Construccion del grafo en forma de cuadricula para las aristas
for indice1 in range(numeroVerticesAlto):
    for indice2 in range(numeroVerticesAncho - 1):
        make_link(grafo, indice1 * numeroVerticesAncho + indice2, indice1 * numeroVerticesAncho + indice2 + 1, np.random.rand())
for indice1 in range(numeroVerticesAlto - 1):
    for indice2 in range(numeroVerticesAncho):
        make_link(grafo, indice1 * numeroVerticesAncho + indice2, indice1 * numeroVerticesAncho + indice2 + numeroVerticesAncho, np.random.rand())

#Construccion del grafo en forma de cuadricula para los nodos
def obtenerPuntos(alto, ancho):
    x = []
    y = []
    for i in range(ancho):
        for j in range(alto):
            x.append(i)
            y.append(j)
    return x, y

def graficarCarreteras(grafo):
    labelBlue = False
    labelGueen = False
    labelYellow = False
    labelOrange = False
    labelRed = False
    transparencia = 0.75
    for i in grafo:
        for j in grafo[i]:
            if i < j:
                x1, y1 = hashNumeroPunto(i, numeroVerticesAlto, numeroVerticesAncho)
                x2, y2 = hashNumeroPunto(j, numeroVerticesAlto, numeroVerticesAncho)
                #Muy poco trafico -> azul
                if grafo[i][j] <= 0.2:
                    if labelBlue == True:
                        plt.plot([x1, x2], [y1, y2], '', c = '#0000ff', alpha = transparencia)
                    else:
                        plt.plot([x1, x2], [y1, y2], '', c = '#0000ff', alpha = transparencia, label = 'Muy poco')
                        labelBlue = True
                #Poco trafico -> verde
                elif grafo[i][j] <= 0.4:
                    if labelGueen == True:
                        plt.plot([x1, x2], [y1, y2], '', c = '#00ff00', alpha = transparencia)
                    else:
                        plt.plot([x1, x2], [y1, y2], '', c = '#00ff00', alpha = transparencia, label = 'Poco')
                        labelGueen = True
                #Trafico regular -> amarillo
                elif grafo[i][j] <= 0.6:
                    if labelYellow == True:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ffff00', alpha = transparencia)
                    else:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ffff00', alpha = transparencia, label = 'Regular')
                        labelYellow = True
                #Trafico pesado -> naranja
                elif grafo[i][j] <= 0.8:
                    if labelOrange == True:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ffbf00', alpha = transparencia)
                    else:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ffbf00', alpha = transparencia, label = 'Pesado')
                        labelOrange = True
                #Trafico muy pesado -> rojo
                elif grafo[i][j] <= 1.0:
                    if labelRed == True:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ff0000', alpha = transparencia)
                    else:
                        plt.plot([x1, x2], [y1, y2], '', c = '#ff0000', alpha = transparencia, label = 'Muy pesado')
                        labelRed = True

print("Coordenada en X del punto inicial (0 <= X < " + str(numeroVerticesAncho) + "):")
#x1 = (int)(sys.stdin.readline())
x1 = 0
print("Coordenada en Y del punto inicial (0 <= Y < " + str(numeroVerticesAlto) + "):")
#y1 = (int)(sys.stdin.readline())
y1 = 0
print("Coordenada en X del punto final (0 <= X < " + str(numeroVerticesAncho) + "):")
#x2 = (int)(sys.stdin.readline())
x2 = 15
print("Coordenada en Y del punto final (0 <= Y < " + str(numeroVerticesAlto) + "):")
#y2 = (int)(sys.stdin.readline())
y2 = 18
x, y = obtenerPuntos(numeroVerticesAlto, numeroVerticesAncho)

#Initialize intial solution
currentSolution = crearRuta(grafo, hashPuntoNumero(x1, y1, numeroVerticesAncho), hashPuntoNumero(x2, y2, numeroVerticesAncho))
print("La animacion terminara despues de " + str(-np.log10(temperatura) / np.log10(tasaEnfriamiento)) + " iteraciones")
print("Distancia de la solucion inicial: " + str(calcularDistanciaRuta(grafo, currentSolution)))

#Set as current best
best = crearRutaModificada(grafo, currentSolution)
#Tour con todos los vertices del grafo con abscisas y ordenadas separadas, y con representacion en numero
fullTourX = []
fullTourY = []
ruta = []
rutaString = ""
valoresEnergeticos = []
valoresTemperatura = []
abscisasTour = [x1, x2]
ordenadasTour = [y1, y2]
plt.ion()
plt.show()
while temperatura > 1:
    plt.clf()
    rutaString = ""
    fullTourX = []
    fullTourY = []
    newSolution = crearRutaModificada(grafo, currentSolution)
    #Get energy of solutions
    currentEnergy = calcularDistanciaRuta(grafo, currentSolution)
    neighbourEnergy = calcularDistanciaRuta(grafo, newSolution)
    #Decide if we should accept the neighbour
    if probabilidadAceptacion(currentEnergy, neighbourEnergy, temperatura) > np.random.rand():
        currentSolution = newSolution
    #Keep track of the best solution found
    if calcularDistanciaRuta(grafo, currentSolution) < calcularDistanciaRuta(grafo, best):
        best = currentSolution
    #Cool system
    temperatura *= tasaEnfriamiento
    number1 = hashPuntoNumero(x1, y1, numeroVerticesAncho)
    number2 = hashPuntoNumero(x2, y2, numeroVerticesAncho)
    ruta = best
    for nodo in ruta:
        coordX, coordY = hashNumeroPunto(nodo, numeroVerticesAlto, numeroVerticesAncho)
        fullTourX.append(coordX)
        fullTourY.append(coordY)
        rutaString += "(" + str(coordY) + ", " + str(coordX) + "), "
    figura1 = plt.subplot(121)
    figura1.plot(x, y, 'w.', markersize = 10)
    figura1.set_xlabel('Eje X')
    figura1.set_ylabel('Eje Y')
    figura1.set_xlim(-margenCiudad, numeroVerticesAncho)
    figura1.set_ylim(-margenCiudad, numeroVerticesAlto)
    graficarCarreteras(grafo)
    figura1.legend(bbox_to_anchor = (0.0, 1.0, 1.0, 0.1), loc = 3, ncol = 5, mode = "expand", borderaxespad = 0.5)
    for label in figura1.legend(bbox_to_anchor = (0.0, 1.0, 1.0, 0.1), loc = 3, ncol = 5, mode = "expand", borderaxespad = 0.5).get_texts():
        label.set_color('w')
    figura1.plot(fullTourY, fullTourX, 'w-', linewidth = 3.5)
    figura1.plot(abscisasTour, ordenadasTour, 'c.', markersize = 25)
    figura2 = plt.subplot(122)
    valoresEnergeticos.append(currentEnergy)
    figura2.plot(valoresEnergeticos, 'c-', label = "Energia", linewidth = 2.5)
    figura2.set_title('Funcion de energia respecto al numero de iteraciones')
    figura2.set_xlabel('Numero de Iteraciones')
    figura2.set_ylabel('Energia')
    figura2.legend(loc = 'upper left')
    for label in figura2.legend(loc = 'upper left').get_texts():
        label.set_color('w')
    plt.pause(tiempoPausa)
    if temperatura <= 1:
        print("Distancia de la solucion final: " + str(calcularDistanciaRuta(grafo, best)))
        print("El tour esta dado por los puntos: " + rutaString[0: len(rutaString) - 2])
    plt.ioff()
    plt.show()
