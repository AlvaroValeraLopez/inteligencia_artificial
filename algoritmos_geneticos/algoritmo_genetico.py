import numpy as np
import random

class AlgoritmoGenetico:
    """
    Implementa un algoritmo genético simple para la búsqueda de un código genético específico.
    """
    def __init__(self, elementos_poblacion=100, max_iteraciones=1000, num_genes=30, prob_mutacion=0.1):
        """
        Constructor de la clase AlgoritmoGenetico.

        Inicializa los parámetros del algoritmo genético, incluyendo el tamaño de la población,
        el número máximo de iteraciones, el número de genes, el código a encontrar,
        la longitud del cromosoma, y la probabilidad de mutación.

        Args:
            elementos_poblacion (int, optional): Tamaño de la población. Por defecto es 100.
            max_iteraciones (int, optional): Número máximo de iteraciones. Por defecto es 1000.
            num_genes (int, optional): Número de genes. Por defecto es 30.
            prob_mutacion (float, optional): Probabilidad de mutación. Por defecto es 0.1.
        """
        self.elementos_poblacion = elementos_poblacion
        self.max_iteraciones = max_iteraciones
        self.num_genes = num_genes
        self.codigo = np.random.randint(1, 100, self.num_genes)
        self.lon_cromosoma = len(self.codigo)
        self.prob_mutacion = prob_mutacion


    def primera_generacion(self):
        """
        Crea la primera generación de la población.

        Genera una lista de cromosomas aleatorios, donde cada cromosoma es un array de números enteros
        y cada número entero es un gen del cromosoma.

        :return: una lista de cromosomas aleatorios.
        """
        return [np.random.randint(1, 100, self.lon_cromosoma) for _ in range(self.elementos_poblacion)]

    def evaluar_cromosoma(self, cromosoma):
        """
        Evalúa un cromosoma.

        Calcula la suma de las diferencias entre los genes del cromosoma y el código objetivo.

        :param cromosoma: el cromosoma a evaluar.
        :return: la suma de las diferencias entre los genes del cromosoma y el código objetivo.
        """
        return np.sum(cromosoma != self.codigo)

    def ordenar_poblacion(self, poblacion):
        """
        Ordena la población en orden ascendente de aptitud.

        :param poblacion: la población a ordenar.
        :return: la población ordenada en orden ascendente de aptitud.
        """
        poblacion.sort(key=self.evaluar_cromosoma)
        return poblacion

    def siguiente_generacion(self, poblacion):
        """
        Crea la siguiente generación de la población.

        Mantiene a la élite (el 10% de la población con la mejor aptitud) y genera el resto de la población
        a través del cruce de un individuo de la élite y un individuo de la población.

        :param poblacion: la población actual.
        :return: la siguiente generación de la población.
        """
        nueva_generacion = []
        elite = poblacion[:self.elementos_poblacion // 10]
        nueva_generacion.extend(elite)
        while len(nueva_generacion) < self.elementos_poblacion:
            padre = random.choice(elite)
            madre = random.choice(poblacion)
            hijo = self.cruzar(padre, madre)
            nueva_generacion.append(hijo)
        return nueva_generacion

    def cruzar(self, padre, madre):
        """
        Cruza dos cromosomas para producir un hijo.

        Selecciona un punto de cruce al azar y combina los genes de los padres en este punto para generar un nuevo cromosoma.

        :param padre: el cromosoma del padre.
        :param madre: el cromosoma de la madre.
        :return: el cromosoma del hijo.
        """
        punto_cruce = random.randint(0, self.lon_cromosoma)
        hijo = np.concatenate((padre[:punto_cruce], madre[punto_cruce:]))
        return hijo

    def mutacion(self, poblacion):
        """
        Muta los cromosomas de la población con una cierta probabilidad.

        Para cada cromosoma en la población, selecciona un punto de mutación al azar y cambia el gen en este punto
        a un nuevo valor al azar con una probabilidad definida por self.prob_mutacion.

        :param poblacion: la población de cromosomas a mutar.
        :return: la población de cromosomas después de la mutación.
        """
        for i in range(len(poblacion)):
            if random.random() < self.prob_mutacion:
                punto_mutacion = random.randint(0, self.lon_cromosoma - 1)
                poblacion[i][punto_mutacion] = random.randint(1, 100)
        return poblacion

    def comprobar_mejor_individuo(self, mejor_individuo):
        """
        Comprueba si un individuo es el mejor individuo posible (es decir, su aptitud es 0).

        :param mejor_individuo: el individuo a comprobar.
        :return: True si el individuo es el mejor individuo posible, False de lo contrario.
        """
        return self.evaluar_cromosoma(mejor_individuo) == 0

    def ejecutar(self):
        """
        Ejecuta el algoritmo genético.

        Inicializa la población y luego entra en un bucle en el que genera la siguiente generación,
        aplica la mutación, y comprueba si el mejor individuo ha sido encontrado. Si se ha encontrado el mejor individuo,
        o si se ha alcanzado el número máximo de iteraciones, el algoritmo se detiene.

        :return: Una lista que contiene: 
            - un booleano que indica si se ha encontrado el mejor individuo, 
            - el valor de fitness del mejor individuo de la última generación, y 
            - el número de iteraciones realizadas.
        """
        poblacion = self.primera_generacion()
        poblacion = self.ordenar_poblacion(poblacion)
        
        if self.comprobar_mejor_individuo(poblacion[0]):
            return [True, 0, 0]
        
        for i in range(self.max_iteraciones):
            poblacion = self.siguiente_generacion(poblacion)
            poblacion = self.mutacion(poblacion)
            poblacion = self.ordenar_poblacion(poblacion)
            
            if self.comprobar_mejor_individuo(poblacion[0]):
                return [True, 0, i+1]
        
        return [False, self.evaluar_cromosoma(poblacion[0]), self.max_iteraciones]

