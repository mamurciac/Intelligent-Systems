import matplotlib.pyplot as plt
import numpy as np

tiempoPausa = 0.1
minimoEjeX = -1
maximoEjeX = 11
minimoEjeY = -1
maximoEjeY = 12

def generarMuestra(numeroAbscisas, pendiente, intercepto):
    muestra = []
    clases = {'1': [], '2': []}
    for x in range(numeroAbscisas):
        epsilon = np.random.rand() % 1 + 0.7
        punto1 = [x, x * pendiente + intercepto + epsilon]
        muestra.append(punto1)
        clases['1'].append(punto1)
        epsilon = np.random.rand() % 1 + 0.7
        punto2 = [x, x * pendiente + intercepto - epsilon]
        muestra.append(punto2)
        clases['2'].append(punto2)
    return muestra, clases

pendiente = 1
intercepto = 0
muestra, clases = generarMuestra(maximoEjeX, pendiente, intercepto)

def revisarClasificacionLineal(clases, clase, w1, w2, b):
    clasificacion = []
    for punto in clases[clase]:
        v = w1 * punto[0] + w2 * punto[1] + b
        if v != 0:
            clasificacion.append(np.sign(v))
        else:
            return 0
    for resultado in clasificacion:
        if resultado != clasificacion[0]:
            return 0
    return np.sign(clasificacion[0])

def separarPuntosPorListasDeCoordenadas(clases, clase):
    x = []
    y = []
    for punto in clases[clase]:
        x.append(punto[0])
        y.append(punto[1])
    return x, y

#Algoritmo de clasificacion para 2 clases linealmente separables
def algoritmoPerceptronSimple(muestra, clase1, clase2):
    w1 = np.random.rand()
    w2 = np.random.rand()
    b = np.random.rand()
    while w1 == 0 or w2 == 0 or b == 0:
        w1 = np.random.rand()
        w2 = np.random.rand()
        b = np.random.rand()
    alfa = 0.001
    plt.ion()
    plt.show()
    numeroPasos = 1
    while True:
        plt.clf()
        parejaSeleccionada = muestra[np.random.randint(len(muestra))]
        z = w1 * parejaSeleccionada[0] + w2 * parejaSeleccionada[1] + b
        if not ((parejaSeleccionada in clase1 and z >= 0) or (parejaSeleccionada in clase2 and z < 0)):
            if z < 0 and parejaSeleccionada in clase1:
                w1 += alfa * parejaSeleccionada[0]
                w2 += alfa * parejaSeleccionada[1]
                b += alfa
            else:
                if z >= 0 and parejaSeleccionada in clase2:
                    w1 -= alfa * parejaSeleccionada[0]
                    w2 -= alfa * parejaSeleccionada[1]
                    b -= alfa
        x1, y1 = separarPuntosPorListasDeCoordenadas(clases, '1')
        x2, y2 = separarPuntosPorListasDeCoordenadas(clases, '2')
        plt.plot(x1, y1, 'bo', label = 'Clase 1 de muestra')
        plt.plot(x2, y2, 'ro', label = 'Clase 2 de muestra')
        listaDeValoresEjeIndependiente = np.arange(minimoEjeX, maximoEjeX, 0.01)
        plt.plot(listaDeValoresEjeIndependiente, -(w1 * listaDeValoresEjeIndependiente + b) / w2, 'g-', label = "Frontera de Decision propuesta por el algoritmo")
        plt.legend(loc = 'upper left')
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Visualizacion de la recta que proporciona el algoritmo')
        plt.xlim(minimoEjeX, maximoEjeX)
        plt.ylim(minimoEjeY, maximoEjeY)
        plt.grid(True)
        plt.pause(tiempoPausa)
        revisionClasificacion1 = revisarClasificacionLineal(clases, '1', w1, w2, b)
        revisionClasificacion2 = revisarClasificacionLineal(clases, '2', w1, w2, b)
        numeroPasos += 1
        if revisionClasificacion1 != 0 and revisionClasificacion2 != 0 and revisionClasificacion1 != revisionClasificacion2:
            print "Fue(ron) necesario(s)", numeroPasos, "paso(s) para obtener una recta de clasificacion"
            print "La recta de clasificacion que proporciona el algoritmo es " + str(w1) + "x + " + str(w2) + "y + " + str(b) + " = 0"
            break
    plt.ioff()
    plt.show()

algoritmoPerceptronSimple(muestra, clases['1'], clases['2'])