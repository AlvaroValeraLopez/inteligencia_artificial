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

def graficar_resultados(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, y='Tiempo', x=df.index, marker='o', color='blue')
    plt.fill_between(df.index, 'Tiempo', color='blue', alpha=0.2, data=df)
    plt.xlabel('Número de prueba')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de ejecución por prueba')
    plt.grid(True)
    plt.show()

def graficar_fitness(df):
    valor = df[df['Encontrado'] == False]['Fitness'].mean()

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
    
    n_pruebas = 10
    resultados_pruebas = pruebas_algoritmo_genetico(n_pruebas)

    graficar_exito(calcula_metricas(resultados_pruebas)[0])
    graficar_resultados(resultados_pruebas)
    graficar_fitness(resultados_pruebas)

