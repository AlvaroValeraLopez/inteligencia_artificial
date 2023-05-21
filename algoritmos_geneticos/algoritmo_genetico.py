import numpy as np
import random

class AlgoritmoGenetico:
    def __init__(self):
        self.elementos_poblacion = 100
        self.max_iteraciones = 1000
        self.num_genes = 30
        self.codigo = np.random.randint(1, 100, self.num_genes)
        self.lon_cromosoma = len(self.codigo)
        self.prob_mutacion = 0.1

    def primera_generacion(self):
        return [np.random.randint(1, 100, self.lon_cromosoma) for _ in range(self.elementos_poblacion)]

    def evaluar_cromosoma(self, cromosoma):
        return np.sum(cromosoma != self.codigo)

    def ordenar_poblacion(self, poblacion):
        poblacion.sort(key=self.evaluar_cromosoma)
        return poblacion

    def siguiente_generacion(self, poblacion):
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
        punto_cruce = random.randint(0, self.lon_cromosoma)
        hijo = np.concatenate((padre[:punto_cruce], madre[punto_cruce:]))
        return hijo

    def mutacion(self, poblacion):
        for i in range(len(poblacion)):
            if random.random() < self.prob_mutacion:
                punto_mutacion = random.randint(0, self.lon_cromosoma - 1)
                poblacion[i][punto_mutacion] = random.randint(1, 100)
        return poblacion

    def comprobar_mejor_individuo(self, mejor_individuo):
        return self.evaluar_cromosoma(mejor_individuo) == 0

    def ejecutar(self):
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

