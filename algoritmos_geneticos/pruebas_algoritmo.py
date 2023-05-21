import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np

import time

from algoritmo_genetico import AlgoritmoGenetico


def graficar_exito(tasa_exito):
    fig, ax = plt.subplots(figsize=(4, 4))
    datos = [1 - tasa_exito, tasa_exito]
    colores = ['white', 'lightblue']
    ax.pie(datos, colors=colores, startangle=90, 
           wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, labels=['', ''])
    ax.text(0, 0, '{:.2f}'.format(tasa_exito * 100), fontsize=30, 
            color='lightblue', ha='center', va='center')
    circulo_central = plt.Circle((0, 0), 0.6, color='white')
    ax.add_artist(circulo_central)
    ax.set_title('Tasa de éxito del algoritmo genético', fontsize=12)
    plt.show()

def graficar_aciertos(n_true, total):
    n_false = total - n_true

    plt.figure(figsize=(8, 6))

    colores = ['lightgreen', 'red']
    valores = [n_true, n_false]
    etiquetas = ['Encontrado', 'No encontrado']

    sns.barplot(x=etiquetas, y=valores, palette=colores, alpha=0.6)

    ax = plt.gca()
    ax.set_axisbelow(True)  # Mover el eje y al fondo

    for i, v in enumerate(valores):
        ax.text(i, v + 0.5, str(v), ha='center')

    plt.title('Resultados de la ejecución del algoritmo genético')
    plt.xlabel('Solución encontrada')
    plt.ylabel('Conteo')
    plt.grid(axis='y', alpha=0.5)

    plt.show()

def graficar_resultados(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, y='Tiempo', x=df.index, marker='o', color='blue')
    plt.fill_between(df.index, 'Tiempo', color='blue', alpha=0.2, data=df)
    plt.xlabel('Número de prueba')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de ejecución por prueba')
    plt.grid(True)
    plt.show()

def graficar_fitness(valor):
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.barh([0], valor, color='lightgreen' if valor > 0 else 'red', 
            height=0.2, align='center', alpha=0.6)
    ax.set_xlim(-max(abs(valor), 1.0), max(abs(valor), 1.0))
    ax.set_ylim(-0.5, 0.5)
    ax.axvline(0, color='black')
    ax.yaxis.set_ticks([])
    ax.set_title('Valor promedio de Fitness para pruebas fallidas')

    for spine in ['left', 'right', 'top', 'bottom']:
        ax.spines[spine].set_visible(False)
    plt.show()

def graficar_iteraciones(df):
    plt.figure(figsize=(10, 6))

    # Dibujar el histograma
    sns.histplot(df[df['Encontrado'] == True]['Iteraciones'], bins=30, color='blue')

    # Ajustar el orden de los elementos del gráfico
    ax = plt.gca()
    ax.set_axisbelow(True)  # Mover el eje y al fondo

    # Configurar etiquetas y título
    plt.xlabel('Número de iteraciones')
    plt.ylabel('Frecuencia')
    plt.title('Distribución del número de iteraciones necesarias para encontrar la solución')

    # Mostrar el grid
    plt.grid(axis='y')

    # Mostrar el gráfico
    plt.show()


def ejecutar_prueba():
    inicio = time.time()

    ag = AlgoritmoGenetico()
    resultado = (ag.ejecutar())

    tiempo = time.time() - inicio
    resultado.insert(0, tiempo)

    return resultado


def pruebas_algoritmo_genetico(n_pruebas):
    resultados = []

    for _ in range(n_pruebas):
        resultados.append(ejecutar_prueba())

    return pd.DataFrame(resultados, columns=['Tiempo', 'Encontrado', 'Fitness', 'Iteraciones'])


def calcula_metricas(df):
    # Tasa de acierto
    tasa_acierto = df['Encontrado'].mean()

    # Corrección Fitness: solo para los casos donde no se encontró la solución
    media_fitness = df[df['Encontrado'] == False]['Fitness'].mean()

    # Numero interaciones: solo para los casos donde se encontró la solución
    media_iteraciones = df[df['Encontrado'] == True]['Iteraciones'].mean()

    return tasa_acierto, media_fitness, media_iteraciones


if __name__ == '__main__':
    
    n_pruebas = 100

    resultados_pruebas = pruebas_algoritmo_genetico(n_pruebas)
    tasa_acierto, media_fitness, media_iteraciones = calcula_metricas(resultados_pruebas)

    graficar_exito(tasa_acierto)
    graficar_aciertos(n_pruebas * tasa_acierto, n_pruebas)
    graficar_resultados(resultados_pruebas)
    graficar_fitness(media_fitness)
    graficar_iteraciones(resultados_pruebas)
