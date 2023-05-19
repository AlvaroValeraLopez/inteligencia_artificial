import random
import numpy as np


# Parámetros del algoritmo
ELEMENTOS_POBLACION = 100  # Tamaño de la población
MAX_ITERACIONES = 1000  # Número máximo de iteraciones
NUM_GENES = 30
CODIGO = np.random.randint(1, 100, NUM_GENES)
LON_CROMOSOMA = len(CODIGO)
PROB_MUTACION = 0.1  # Probabilidad de mutación


def primeraGeneracion():
    """
    Función para generar la población inicial de cromosomas. Cada cromosoma es un vector de enteros 
    generados aleatoriamente.

    :return: lista de cromosomas (numpy arrays)
    """
    return [np.random.randint(1, 100, LON_CROMOSOMA) for _ in range(ELEMENTOS_POBLACION)]


def evaluarCromosoma(cromosoma):
    """
    Función para evaluar la aptitud de un cromosoma. La aptitud se calcula como la suma de las diferencias 
    entre los genes del cromosoma y los del código objetivo.

    :param cromosoma: Un array de numpy que representa un cromosoma.
    :return: un entero que representa la aptitud del cromosoma.
    """
    return np.sum(cromosoma != CODIGO)


def ordenarPoblacion(poblacion):
    """
    Función para ordenar la población de cromosomas en orden ascendente de aptitud.

    :param poblacion: Lista de cromosomas.
    :return: La población ordenada.
    """
    poblacion.sort(key=evaluarCromosoma)
    return poblacion


def siguienteGeneracion(poblacion):
    """
    Función para generar la próxima generación de cromosomas a partir de la población actual.

    :param poblacion: Lista de cromosomas que representan la población actual.
    :return: Nueva generación de cromosomas.
    """
    nueva_generacion = []  # Lista para la nueva generación
    elite = poblacion[:ELEMENTOS_POBLACION // 10]  # Selección del 10% de los mejores individuos
    nueva_generacion.extend(elite)  # La élite pasa directamente a la siguiente generación
    
    # Completamos la población con descendencia de individuos elegidos de la élite y la población
    while len(nueva_generacion) < ELEMENTOS_POBLACION:
        padre = random.choice(elite)
        madre = random.choice(poblacion)
        hijo = cruzar(padre, madre)
        nueva_generacion.append(hijo)

    return nueva_generacion


def cruzar(padre, madre):
    """
    Función para cruzar dos cromosomas. La descendencia se genera tomando la primera parte del padre 
    y la segunda parte de la madre.

    :param padre: Un array de numpy que representa un cromosoma.
    :param madre: Un array de numpy que representa un cromosoma.
    :return: Un nuevo cromosoma generado a partir de los cromosomas del padre y la madre.
    """
    punto_cruce = random.randint(0, LON_CROMOSOMA)
    hijo = np.concatenate((padre[:punto_cruce], madre[punto_cruce:]))
    return hijo


def mutacion(poblacion):
    """
    Función para aplicar una mutación aleatoria a los cromosomas de la población.

    :param poblacion: Lista de cromosomas.
    :return: La población con cromosomas posiblemente mutados.
    """
    for i in range(len(poblacion)):
        if random.random() < PROB_MUTACION:
            punto_mutacion = random.randint(0, LON_CROMOSOMA - 1)
            poblacion[i][punto_mutacion] = random.randint(1, 100)
    return poblacion

def comprobarMejorIndividuo(mejor_individuo):
    return evaluarCromosoma(mejor_individuo) == 0

def algoritmo_genetico():
    """
    Función principal que controla el flujo del algoritmo genético. 

    :return: El cromosoma que coincide con el código objetivo, o None si no se encuentra tal cromosoma después del número máximo de iteraciones.
    """
    poblacion = primeraGeneracion()
    poblacion = ordenarPoblacion(poblacion)
    # Si el mejor individuo es igual al código, se ha encontrado la solución
    if comprobarMejorIndividuo(poblacion[0]): return poblacion[0] 

    for _ in range(MAX_ITERACIONES):
        poblacion = siguienteGeneracion(poblacion)
        poblacion = mutacion(poblacion)
        poblacion = ordenarPoblacion(poblacion)

        # Si el mejor individuo es igual al código, se ha encontrado la solución
        if comprobarMejorIndividuo(poblacion[0]): return True, poblacion[0] 

    # Si se llega al número máximo de iteraciones y no se ha encontrado la solución, se informa y se termina
    return False, None


if __name__ == '__main__':

    print('El código buscado es:', CODIGO, sep='\n')

    # Ejecutar el algoritmo genético
    encontrado, individuo = algoritmo_genetico()

    if encontrado: print("\nCódigo encontrado!", individuo, sep='\n')
    else: print("\nCódigo no encontrado en las iteraciones máximas.")

