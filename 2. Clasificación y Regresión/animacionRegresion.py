from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

tiempoPausa = 0.1

minimoEjeX = -1
maximoEjeX = 5
minimoEjeY = -1
maximoEjeY = 5
minimoEjeZ = -1
maximoEjeZ = 11

def generarMuestra(numeroAbscisas1, numeroAbscisas2, pendiente1, pendiente2, intercepto):
    muestra = []
    i = 0
    for x in range(numeroAbscisas1):
        for y in range(numeroAbscisas2):
            epsilon = np.random.rand() % 1
            if i % 2 == 0:
                muestra.append([x, y, x * pendiente1 + y * pendiente2 + intercepto + epsilon])
            else:
                muestra.append([x, y, x * pendiente1 + y * pendiente2 + intercepto - epsilon])
            i += 1
    return muestra

def calcularErrorTotalMinimo(muestra, pendiente1, pendiente2, intercepto):
    errorTotal = 0
    for punto in muestra:
        errorTotal += abs(punto[2] - (punto[0] * pendiente1 + punto[1] * pendiente2 + intercepto))
    return errorTotal / len(muestra)

pendiente1 = 1
pendiente2 = 1
intercepto = 0
muestra = generarMuestra(maximoEjeX, maximoEjeY, pendiente1, pendiente2, intercepto)
           
def separarPuntosPorListasDeCoordenadas(muestra):
    x = []
    y = []
    z = []
    for punto in muestra:
        x.append(punto[0])
        y.append(punto[1])
        z.append(punto[2])
    return x, y, z

def planoRegresion(x, y, w1, w2, b):
    valoresEnElPlano = []
    for indice in range(len(x)):
        valoresEnElPlano.append(w1 * x[indice] + w2 * y[indice] + b)
    return valoresEnElPlano

fig = plt.figure()
ax = fig.gca(projection = '3d')

def algoritmoAdaline(muestra, tasaAprendizaje):
    #Calculo del error minimo y un sesgo como margen de error
    errorMinimo = calcularErrorTotalMinimo(muestra, pendiente1, pendiente2, intercepto)
    epsilonError = 0.05
    print "Error minimo = " + str(errorMinimo)
    print "Margen de error = " + str(epsilonError)
    print "Error objetivo = " + str(errorMinimo + epsilonError)
    #Desarrollo del algoritmo Adaline (Pesos aleatorios entre -5 y 5)
    w1 = np.random.rand() % 10 - 5
    w2 = np.random.rand() % 10 - 5
    b = np.random.rand() % 10 - 5
    numeroPasos = 1
    plt.ion()
    plt.show()
    while True:
        ax.cla()
        errorTotal = 0
        for punto in muestra:
            v = w1 * punto[0] + w2 * punto[1] + b
            error = punto[2] - v
            errorTotal += abs(error)
            b = b + tasaAprendizaje * error
            w1 = w1 + tasaAprendizaje * error * punto[0]
            w2 = w2 + tasaAprendizaje * error * punto[1]
        errorTotal = errorTotal / len(muestra)
        print "Error en la iteracion " + str(numeroPasos) + " = " + str(errorTotal)
        x, y, z = separarPuntosPorListasDeCoordenadas(muestra)
        #Ilustracion de los puntos de muestra
        ax.plot(np.array(x), np.array(y), np.array(z), 'b.')
        #Puntos demas para mostrar mejor el plano de regresion
        x.append(minimoEjeX)
        x.append(maximoEjeX)
        y.append(minimoEjeY)
        y.append(maximoEjeY)
        x.append(minimoEjeX)
        x.append(maximoEjeX)
        y.append(maximoEjeY)
        y.append(minimoEjeY)
        # Ilustracion del plano de regresion
        ax.plot_trisurf(x, y, np.array(planoRegresion(x, y, w1, w2, b)), color = 'r', alpha = 0.25)
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('Eje Z')
        ax.set_xlim(minimoEjeX, maximoEjeX)
        ax.set_ylim(minimoEjeY, maximoEjeY)
        ax.set_zlim(minimoEjeZ, maximoEjeZ)
        ax.set_title('Visualizacion del plano que proporciona el algoritmo')
        plt.pause(tiempoPausa)
        if errorTotal <= errorMinimo + epsilonError:
            print "Fue(ron) necesario(s)", numeroPasos, "paso(s) para obtener un plano de regresion"
            print "El plano de regresion que proporciona el algoritmo es z = " + str(w1) + "x + " + str(w2) + "y + " + str(b)
            break
        numeroPasos += 1
    plt.ioff()
    plt.show()

algoritmoAdaline(muestra, 0.01)