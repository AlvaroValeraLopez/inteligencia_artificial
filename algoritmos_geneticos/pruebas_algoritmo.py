import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import time

from algoritmo_genetico import AlgoritmoGenetico

def pruebas_algoritmo_genetico(n_pruebas):
    resultados = []
    exitos = 0
    aptitudes = []
    for _ in range(n_pruebas):
        inicio = time.time()
        ag = AlgoritmoGenetico()
        encontrado, individuo, iteraciones, mejores_aptitudes = ag.ejecutar()
        tiempo = time.time() - inicio
        acierto = np.sum(individuo == ag.codigo) / ag.lon_cromosoma if individuo is not None else 0
        resultados.append([tiempo, acierto, iteraciones])
        aptitudes.append(mejores_aptitudes) # Agregamos las aptitudes del mejor individuo en cada generación
        if encontrado: exitos += 1
    tasa_exito = exitos / n_pruebas
    return pd.DataFrame(resultados, columns=['tiempo', 'acierto', 'iteraciones']), tasa_exito, aptitudes

def graficar_aptitudes(aptitudes):
    plt.figure(figsize=(12, 6))
    for i, aptitud in enumerate(aptitudes):
        plt.plot(aptitud, label=f'Prueba {i+1}')
    plt.xlabel('Generaciones')
    plt.ylabel('Aptitud')
    plt.title('Aptitud del mejor individuo por generación')
    plt.legend(loc='upper right')
    plt.grid(True)  # Agregamos una cuadrícula al gráfico
    plt.show()

def graficarExito(tasa_exito):
    fig, ax = plt.subplots(figsize=(4, 4))
    datos = [1 - tasa_exito, tasa_exito]
    colores = ['white', 'lightblue']
    ax.pie(datos, colors=colores, startangle=90, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, labels=['', ''])
    ax.text(0, 0, '{:.2f}'.format(tasa_exito * 100), fontsize=30, color='lightblue', ha='center', va='center')
    circulo_central = plt.Circle((0, 0), 0.6, color='white')
    ax.add_artist(circulo_central)
    ax.set_title('Tasa de éxito del algoritmo genético', fontsize=12)
    plt.show()

def graficar_resultados(resultados):
    plt.figure(figsize=(12, 6))
    plt.plot(resultados['tiempo'], marker='o')
    plt.xlabel('Número de prueba')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de ejecución por prueba')
    plt.fill_between(np.arange(len(resultados['tiempo'])), resultados['tiempo'], color='blue', alpha=0.2)

    # Obtener las marcas en el eje y
    marcas_y = np.arange(0, max(resultados['tiempo']) + 0.1, 0.1)

    # Agregar líneas horizontales en cada marca de valor en el eje y
    plt.hlines(marcas_y, 0, len(resultados['tiempo']) - 1, color='gray', linestyle='--', linewidth=0.5)
    
    plt.grid(True)  # Agregamos una cuadrícula al gráfico
    plt.show()

def plot_value_bar(value):
    fig, ax = plt.subplots()

    # Configuración de los límites del eje x
    ax.set_xlim(-max(abs(value), 1.0), max(abs(value), 1.0))

    # Configuración de los límites del eje y
    ax.set_ylim(-0.5, 0.5)

    # Dibujar la línea en el 0
    ax.axvline(0, color='black')

    # Dibujar la barra de valor
    if value > 0:
        ax.barh(0, value, color='lightgreen', height=0.2)
    elif value < 0:
        ax.barh(0, value, color='red', height=0.2)

    # Configuración de los ejes
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_ticks([])

    plt.show()

if __name__ == '__main__':
    # n_pruebas = 10
    # resultados, tasa_exito, aptitudes = pruebas_algoritmo_genetico(n_pruebas)
    # graficar_resultados(resultados)
    # graficarExito(tasa_exito)
    # graficar_aptitudes(aptitudes)
    # Ejemplo de uso
    valor = 2.5  # Puedes cambiar este valor para probar diferentes casos
    plot_value_bar(valor)
