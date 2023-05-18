import random

# Parámetros del algoritmo genético
TAM_POBLACION = 100  # Tamaño de la población
LONGITUD_CROMOSOMA = 10  # Longitud del cromosoma
NUM_GENERACIONES = 100  # Número de generaciones
ELITE_PORCENTAJE = 0.1  # Porcentaje de élite
PROB_MUTACION = 0.1  # Probabilidad de mutación
MAX_ITERACIONES = 1000  # Número máximo de iteraciones

# Código objetivo
codigo_objetivo = [5, 17, 92, 43, 78, 32, 66, 10, 55, 25]

class Cromosoma:
    def __init__(self):
        self.genes = [random.randint(1, 100) for _ in range(LONGITUD_CROMOSOMA)]
        self.fitness = 0

def calcular_fitness(cromosoma):
    return sum(1 for i, j in zip(cromosoma.genes, codigo_objetivo) if i != j)

def primera_generacion():
    return [Cromosoma() for _ in range(TAM_POBLACION)]

def ordenar_poblacion(poblacion):
    poblacion.sort(key=lambda cromosoma: cromosoma.fitness)

def seleccion(poblacion):
    elite_size = int(TAM_POBLACION * ELITE_PORCENTAJE)
    elite = poblacion[:elite_size]
    seleccionados = elite.copy()
    for _ in range(TAM_POBLACION - elite_size):
        padre1 = random.choice(elite)
        padre2 = random.choice(poblacion)
        seleccionados.append(padre2 if padre1.fitness < padre2.fitness else padre1)
    return seleccionados

def cruzamiento(padres):
    hijos = []
    for i in range(0, TAM_POBLACION, 2):
        punto_corte = random.randint(1, LONGITUD_CROMOSOMA - 1)
        hijo1 = Cromosoma()
        hijo2 = Cromosoma()
        hijo1.genes = padres[i].genes[:punto_corte] + padres[i + 1].genes[punto_corte:]
        hijo2.genes = padres[i + 1].genes[:punto_corte] + padres[i].genes[punto_corte:]
        hijos.extend([hijo1, hijo2])
    return hijos

def mutacion(poblacion):
    for cromosoma in poblacion:
        for i in range(LONGITUD_CROMOSOMA):
            if random.random() < PROB_MUTACION:
                cromosoma.genes[i] = random.randint(1, 100)

def algoritmo_genetico():
    poblacion = primera_generacion()
    mejor_fitness = float('inf')
    iteracion = 0

    while mejor_fitness > 0 and iteracion < MAX_ITERACIONES:
        for cromosoma in poblacion:
            cromosoma.fitness = calcular_fitness(cromosoma)

        ordenar_poblacion(poblacion)
        mejor_cromosoma = poblacion[0]
        mejor_fitness = mejor_cromosoma.fitness

        print(f"Iteración {iteracion + 1}: Fitness={mejor_fitness}, Cromosoma={mejor_cromosoma.genes}")

        seleccionados = seleccion(poblacion)
        hijos = cruzamiento(seleccionados)
        mutacion(hijos)
        ordenar_poblacion(hijos)
        poblacion = hijos[:TAM_POBLACION]
        iteracion += 1

    if mejor_fitness == 0:
        print("¡Se ha encontrado la solución!")
    else:
        print("Se ha alcanzado el número máximo de iteraciones sin encontrar la solución.")


if __name__ == '__main__':
    # Ejecutar el algoritmo genético
    poblacion = primera_generacion()
    mejor_fitness = float('inf')
    iteracion = 0

    while mejor_fitness > 0 and iteracion < MAX_ITERACIONES:
        for cromosoma in poblacion:
            cromosoma.fitness = calcular_fitness(cromosoma)

        ordenar_poblacion(poblacion)
        mejor_cromosoma = poblacion[0]
        mejor_fitness = mejor_cromosoma.fitness

        print(f"Iteración {iteracion + 1}: Fitness={mejor_fitness}, Cromosoma={mejor_cromosoma.genes}")

        seleccionados = seleccion(poblacion)
        hijos = cruzamiento(seleccionados)
        mutacion(hijos)
        ordenar_poblacion(hijos)
        poblacion = hijos[:TAM_POBLACION]
        iteracion += 1

    if mejor_fitness == 0:
        print("¡Se ha encontrado la solución!")
    else:
        print("Se ha alcanzado el número máximo de iteraciones sin encontrar la solución.")