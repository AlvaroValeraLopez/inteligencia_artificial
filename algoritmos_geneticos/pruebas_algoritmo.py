import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time
from algoritmo_genetico import AlgoritmoGenetico


# Ruta de la carpeta de graficos.
GRAFICO_DIR = 'graphs/'


def graficar_exito(tasa_exito):
    """
    Esta función genera un gráfico de pastel que muestra la tasa de éxito de la ejecución del algoritmo genético.
    Args:
        tasa_exito (float): La tasa de éxito del algoritmo genético.
    """
    fig, ax = plt.subplots(figsize=(4, 4))
    datos = [1 - tasa_exito, tasa_exito]
    colores = ['white', 'lightblue']
    ax.pie(datos, colors=colores, startangle=90, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, labels=['', ''])
    ax.text(0, 0, '{:.2f}'.format(tasa_exito * 100), fontsize=30, color='lightblue', ha='center', va='center')
    circulo_central = plt.Circle((0, 0), 0.6, color='white')
    ax.add_artist(circulo_central)
    ax.set_title('Tasa de éxito del algoritmo genético', fontsize=12)
    plt.savefig('{}grafico_exito.png'.format(GRAFICO_DIR))
    plt.show()

def graficar_aciertos(n_true, total):
    """
    Esta función genera un gráfico de barras que muestra el número de soluciones encontradas y no encontradas.
    Args:
        n_true (int): Número de soluciones encontradas.
        total (int): Número total de ejecuciones.
    """
    n_false = total - n_true
    plt.figure(figsize=(8, 6))
    colores = ['lightgreen', 'red']
    valores = [n_true, n_false]
    etiquetas = ['Encontrado', 'No encontrado']
    sns.barplot(x=etiquetas, y=valores, palette=colores, alpha=0.6)
    ax = plt.gca()
    ax.set_axisbelow(True)
    for i, v in enumerate(valores):
        ax.text(i, v + 0.5, str(v), ha='center')
    plt.title('Resultados de la ejecución del algoritmo genético')
    plt.xlabel('Solución encontrada')
    plt.ylabel('Conteo')
    plt.grid(axis='y', alpha=0.5)
    plt.savefig('{}grafico_aciertos.png'.format(GRAFICO_DIR))
    plt.show()

def graficar_resultados(df):
    """
    Esta función genera un gráfico de líneas que muestra el tiempo de ejecución por prueba.
    Args:
        df (DataFrame): DataFrame que contiene los resultados de las pruebas.
    """
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, y='Tiempo', x=df.index, marker='o', color='blue')
    plt.fill_between(df.index, 'Tiempo', color='blue', alpha=0.2, data=df)
    plt.xlabel('Número de prueba')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de ejecución por prueba')
    plt.grid(True)
    plt.savefig('{}grafico_resultados.png'.format(GRAFICO_DIR))
    plt.show()

def graficar_fitness(valor):
    """
    Esta función genera un gráfico de barras horizontal que muestra el valor promedio de Fitness para las pruebas fallidas.
    Args:
        valor (float): Valor promedio de Fitness para las pruebas fallidas.
    """
    fig, ax = plt.subplots(figsize=(5, 2))
    bar = ax.barh([0], valor, color='lightgreen' if valor > 0 else 'red', 
            height=0.2, align='center', alpha=0.6)
    ax.set_xlim(-max(abs(valor), 1.0), max(abs(valor), 1.0))
    ax.set_ylim(-0.5, 0.5)
    ax.axvline(0, color='black')
    ax.yaxis.set_ticks([])
    ax.set_title('Valor promedio de Fitness para pruebas fallidas')

    for spine in ['left', 'right', 'top', 'bottom']:
        ax.spines[spine].set_visible(False)
    
    # Aquí es donde se agrega el valor a la derecha de la barra.
    # bar[0].get_width() nos da la longitud de la barra y bar[0].get_y() nos da la posición y de la barra.
    ax.text(bar[0].get_width(), bar[0].get_y(), str(valor), va='center')
    plt.show()
        
def graficar_iteraciones(df):
    """
    Esta función genera un histograma que muestra la distribución del número de iteraciones necesarias para encontrar la solución.
    Args:
        df (DataFrame): DataFrame que contiene los resultados de las pruebas.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[df['Encontrado'] == True]['Iteraciones'], bins=30, color='blue')
    ax = plt.gca()
    ax.set_axisbelow(True)
    plt.xlabel('Número de iteraciones')
    plt.ylabel('Frecuencia')
    plt.title('Distribución del número de iteraciones necesarias para encontrar la solución')
    plt.grid(axis='y')
    plt.savefig('{}grafico_iteraciones.png'.format(GRAFICO_DIR))
    plt.show()

def ejecutar_prueba():
    """
    Esta función ejecuta una prueba del algoritmo genético y devuelve los resultados.
    Returns:
        list: Una lista que contiene los resultados de la prueba.
    """
    inicio = time.time()
    ag = AlgoritmoGenetico()
    resultado = (ag.ejecutar())
    tiempo = time.time() - inicio
    resultado.insert(0, tiempo)
    return resultado

def pruebas_algoritmo_genetico(n_pruebas):
    """
    Esta función ejecuta un número dado de pruebas del algoritmo genético y devuelve los resultados en un DataFrame.
    Args:
        n_pruebas (int): Número de pruebas a realizar.
    Returns:
        DataFrame: Un DataFrame que contiene los resultados de las pruebas.
    """
    resultados = []
    for _ in range(n_pruebas):
        resultados.append(ejecutar_prueba())
    return pd.DataFrame(resultados, columns=['Tiempo', 'Encontrado', 'Fitness', 'Iteraciones'])

def calcula_metricas(df):
    """
    Esta función calcula la tasa de acierto, la media de Fitness para los casos donde no se encontró la solución y la media de iteraciones para los casos donde se encontró la solución.
    Args:
        df (DataFrame): DataFrame que contiene los resultados de las pruebas.
    Returns:
        tuple: Un tuple que contiene la tasa de acierto, la media de Fitness y la media de iteraciones.
    """
    tasa_acierto = df['Encontrado'].mean()
    media_fitness = df[df['Encontrado'] == False]['Fitness'].mean()
    print(df[df['Encontrado'] == False]['Fitness'])
    media_iteraciones = df[df['Encontrado'] == True]['Iteraciones'].mean()
    return tasa_acierto, media_fitness, media_iteraciones

if __name__ == '__main__':
    """
    El punto de entrada del script. Realiza un número dado de pruebas del algoritmo genético, calcula varias métricas a partir de los resultados y genera gráficos para visualizar los resultados.
    """
    n_pruebas = 5_00
    resultados_pruebas = pruebas_algoritmo_genetico(n_pruebas)
    tasa_acierto, media_fitness, media_iteraciones = calcula_metricas(resultados_pruebas)

    graficar_exito(tasa_acierto)
    graficar_aciertos(n_pruebas * tasa_acierto, n_pruebas)
    graficar_resultados(resultados_pruebas)
    graficar_fitness(media_fitness)
    graficar_iteraciones(resultados_pruebas)
