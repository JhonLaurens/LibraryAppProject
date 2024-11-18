# Archivo: modules/analisis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import logging

class AnalisisEstadistico:
    def __init__(self, df):
        self.df = df

    def analizar_variable(self, muestra, columna):
        try:
            resultados = {}
            datos = muestra[columna]

            if pd.api.types.is_numeric_dtype(datos):
                resultados['media'] = datos.mean()
                resultados['mediana'] = datos.median()
                resultados['moda'] = datos.mode().iloc[0] if not datos.mode().empty else None
                resultados['desv_std'] = datos.std()
                resultados['varianza'] = datos.var()
                resultados['coef_var'] = (resultados['desv_std'] / resultados['media']) * 100 if resultados['media'] != 0 else 0

                # Gráfico de curva normal
                plt.figure(figsize=(10, 6))
                sns.histplot(datos, kde=True, stat="density", color="skyblue")
                xmin, xmax = plt.xlim()
                x = np.linspace(xmin, xmax, 100)
                p = stats.norm.pdf(x, resultados['media'], resultados['desv_std'])
                plt.plot(x, p, 'k', linewidth=2)
                plt.title(f'Curva Normal de {columna}')
                plt.xlabel(columna)
                plt.ylabel('Densidad')
                plt.savefig('grafico_normal.png')
                plt.close()

                # Gráfico de caja y bigotes
                plt.figure(figsize=(8, 6))
                sns.boxplot(x=datos, color='lightgreen')
                plt.title(f'Diagrama de Caja y Bigotes de {columna}')
                plt.xlabel(columna)
                plt.savefig('grafico_caja.png')
                plt.close()

                # Cálculo de probabilidades según distribuciones
                resultados['prob_binomial'] = self.calcular_probabilidad_binomial(datos)
                resultados['prob_poisson'] = self.calcular_probabilidad_poisson(datos)
                resultados['prob_normal'] = self.calcular_probabilidad_normal(datos)
                resultados['prob_hipergeometrica'] = self.calcular_probabilidad_hipergeometrica(datos)

            else:
                frecuencias = datos.value_counts()
                resultados['frecuencias'] = frecuencias
                resultados['moda'] = datos.mode().iloc[0] if not datos.mode().empty else None

                # Gráfico de barras
                plt.figure(figsize=(10, 6))
                frecuencias.plot(kind='bar', color='skyblue')
                plt.title(f'Frecuencias de {columna}')
                plt.xlabel(columna)
                plt.ylabel('Frecuencia')
                plt.savefig('grafico_barras.png')
                plt.close()

            return resultados
        except Exception as e:
            logging.exception(f"Error al analizar la variable {columna}")
            raise e

    # Métodos para calcular probabilidades según distribuciones

    def calcular_probabilidad_binomial(self, datos):
        try:
            n = len(datos)
            p = datos.mean() / n
            k = sum(datos)
            prob = stats.binom.pmf(k, n, p)
            return prob
        except Exception as e:
            logging.exception("Error al calcular probabilidad binomial")
            return None

    def calcular_probabilidad_poisson(self, datos):
        try:
            lambda_ = datos.mean()
            k = int(lambda_)
            prob = stats.poisson.pmf(k, lambda_)
            return prob
        except Exception as e:
            logging.exception("Error al calcular probabilidad Poisson")
            return None

    def calcular_probabilidad_normal(self, datos):
        try:
            mu = datos.mean()
            sigma = datos.std()
            prob = stats.norm.cdf(mu + sigma) - stats.norm.cdf(mu - sigma)
            return prob
        except Exception as e:
            logging.exception("Error al calcular probabilidad Normal")
            return None

    def calcular_probabilidad_hipergeometrica(self, datos):
        try:
            N = len(self.df)
            n = len(datos)
            K = datos.sum()
            k = sum(datos)
            prob = stats.hypergeom.pmf(k, N, K, n)
            return prob
        except Exception as e:
            logging.exception("Error al calcular probabilidad Hipergeométrica")
            return None

    # Métodos para calcular probabilidad conjunta, condicional y teorema de Bayes

    def calcular_probabilidad_conjunta(self, columna1, columna2):
        try:
            conjunta = pd.crosstab(self.df[columna1], self.df[columna2], normalize=True)
            return conjunta
        except Exception as e:
            logging.exception("Error al calcular probabilidad conjunta")
            return None

    def calcular_probabilidad_condicional(self, columna_evento, columna_condicion):
        try:
            conjunta = pd.crosstab(self.df[columna_evento], self.df[columna_condicion], normalize='columns')
            return conjunta
        except Exception as e:
            logging.exception("Error al calcular probabilidad condicional")
            return None

    def aplicar_teorema_bayes(self, A_dado_B, B):
        try:
            # Asumiendo que A_dado_B y B son probabilidades
            P_B_dado_A = (A_dado_B * B) / B
            return P_B_dado_A
        except Exception as e:
            logging.exception("Error al aplicar el Teorema de Bayes")
            return None