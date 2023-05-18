import random
import numpy as np


# Parámetros del algoritmo
ELEMENTOS_POBLACION = 100  # Tamaño de la población
MAX_ITERACIONES = 1000  # Número máximo de iteraciones
NUM_GENES = 30
CODIGO = np.random.randint(1, 100, NUM_GENES)
LON_CROMOSOMA = len(CODIGO)
PROB_MUTACION = 0.1  # Probabilidad de mutación


# Creación de la población inicial con cromosomas generados aleatoriamente
def primeraGeneracion():
    return [np.random.randint(1, 100, LON_CROMOSOMA) for _ in range(ELEMENTOS_POBLACION)]

# Cálculo del fitness de un cromosoma, se cuenta el número de dígitos que difieren del código objetivo
def evaluarCromosoma(cromosoma):
    return np.sum(cromosoma != CODIGO)

# Ordenar la población por su fitness (los individuos con menor fitness, es decir, más parecidos al código, primero)
def ordenarPoblacion(poblacion):
    poblacion.sort(key=evaluarCromosoma)
    return poblacion

# Creación de la siguiente generación a partir de la generación actual
def siguienteGeneracion(poblacion):
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

# Cruce de dos cromosomas, se toma una parte del padre y una del madre
def cruzar(padre, madre):
    punto_cruce = random.randint(0, LON_CROMOSOMA)
    hijo = np.concatenate((padre[:punto_cruce], madre[punto_cruce:]))
    return hijo

# Mutación de la población, con una probabilidad definida, un cromosoma puede mutar (cambiar un dígito aleatoriamente)
def mutacion(poblacion):
    for i in range(len(poblacion)):
        if random.random() < PROB_MUTACION:
            punto_mutacion = random.randint(0, LON_CROMOSOMA - 1)
            poblacion[i][punto_mutacion] = random.randint(1, 100)
    return poblacion

# Algoritmo principal que controla el flujo del proceso evolutivo
def algoritmo_genetico():
    poblacion = primeraGeneracion()
    poblacion = ordenarPoblacion(poblacion)

    for _ in range(MAX_ITERACIONES):
        poblacion = siguienteGeneracion(poblacion)
        poblacion = mutacion(poblacion)
        poblacion = ordenarPoblacion(poblacion)

        # Si el mejor individuo es igual al código, se ha encontrado la solución
        if evaluarCromosoma(poblacion[0]) == 0:
            print("Código encontrado!")
            print(poblacion[0])
            return poblacion[0]

    # Si se llega al número máximo de iteraciones y no se ha encontrado la solución, se informa y se termina
    print("Código no encontrado en las iteraciones máximas.")
    return None


if __name__ == '__main__':
    # Ejecutar el algoritmo genético
    algoritmo_genetico()
