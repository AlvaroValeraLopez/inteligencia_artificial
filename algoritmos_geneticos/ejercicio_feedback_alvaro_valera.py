import random
import numpy as np

# Parámetros del algoritmo
ELEMENTOS_POBLACION = 100
MAX_ITERACIONES = 1000
CODIGO = np.array([30, 1, 50, 77, 85, 99, 2, 8, 40, 22])  # Ejemplo de código a buscar
LON_CROMOSOMA = len(CODIGO)
PROB_MUTACION = 0.1

# Creación de la población inicial
def primeraGeneracion():
    return [np.random.randint(1, 100, LON_CROMOSOMA) for _ in range(ELEMENTOS_POBLACION)]

# Cálculo del fitness
def evaluarCromosoma(cromosoma):
    return np.sum(cromosoma != CODIGO)

# Ordenar la población
def ordenarPoblacion(poblacion):
    poblacion.sort(key=evaluarCromosoma)
    return poblacion

# Creación de la siguiente generación
def siguienteGeneracion(poblacion):
    nueva_generacion = []
    elite = poblacion[:ELEMENTOS_POBLACION // 10]
    nueva_generacion.extend(elite)
    
    while len(nueva_generacion) < ELEMENTOS_POBLACION:
        padre = random.choice(elite)
        madre = random.choice(poblacion)
        hijo = cruzar(padre, madre)
        nueva_generacion.append(hijo)

    return nueva_generacion

# Cruce de dos individuos
def cruzar(padre, madre):
    punto_cruce = random.randint(0, LON_CROMOSOMA)
    hijo = np.concatenate((padre[:punto_cruce], madre[punto_cruce:]))
    return hijo

# Mutación
def mutacion(poblacion):
    for i in range(len(poblacion)):
        if random.random() < PROB_MUTACION:
            punto_mutacion = random.randint(0, LON_CROMOSOMA - 1)
            poblacion[i][punto_mutacion] = random.randint(1, 100)
    return poblacion

# Algoritmo principal
def algoritmo_genetico():
    poblacion = primeraGeneracion()
    poblacion = ordenarPoblacion(poblacion)

    for _ in range(MAX_ITERACIONES):
        poblacion = siguienteGeneracion(poblacion)
        poblacion = mutacion(poblacion)
        poblacion = ordenarPoblacion(poblacion)

        if evaluarCromosoma(poblacion[0]) == 0:
            print("Código encontrado!")
            print(poblacion[0])
            return poblacion[0]

    print("Código no encontrado en las iteraciones máximas.")
    return None

if __name__ == '__main__':
    # Ejecutar el algoritmo genético
    algoritmo_genetico()
