# Archivo: modules/analisis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import logging
import os
from fpdf import FPDF  # Biblioteca para generar PDFs

class AnalisisEstadistico:
    """
    Clase para realizar análisis estadísticos sobre un DataFrame de pandas.
    """

    def __init__(self, df):
        """
        Inicializa la clase con un DataFrame.

        :param df: DataFrame que contiene los datos a analizar.
        """
        self.df = df

    def analizar_variable(self, muestra, columna):
        """
        Analiza una variable del DataFrame y genera resultados estadísticos y gráficos.

        :param muestra: DataFrame de muestra a analizar.
        :param columna: Nombre de la columna a analizar.
        :return: Diccionario con los resultados del análisis.
        """
        try:
            resultados = {}
            datos = muestra[columna]

            if pd.api.types.is_numeric_dtype(datos):
                # Cálculos estadísticos
                resultados['media'] = datos.mean()
                resultados['mediana'] = datos.median()
                resultados['moda'] = datos.mode().iloc[0] if not datos.mode().empty else None
                resultados['desv_std'] = datos.std()
                resultados['varianza'] = datos.var()
                if resultados['media'] != 0:
                    resultados['coef_var'] = (resultados['desv_std'] / resultados['media']) * 100
                else:
                    resultados['coef_var'] = 0

                # Gráfico de distribución con KDE
                plt.figure(figsize=(10, 6))
                sns.histplot(datos, kde=True, stat="density", color="skyblue")
                plt.title(f'Distribución de {columna}')
                plt.xlabel(columna)
                plt.ylabel('Densidad')
                ruta_graficos_distribucion = os.path.join('graficos', f'distribucion_{columna}.png')
                plt.savefig(ruta_graficos_distribucion)
                plt.close()
                resultados['grafico_distribucion'] = ruta_graficos_distribucion

                # Gráfico de caja y bigotes
                plt.figure(figsize=(8, 6))
                sns.boxplot(x=datos, color='lightgreen')
                plt.title(f'Diagrama de Caja y Bigotes de {columna}')
                plt.xlabel(columna)
                ruta_graficos_caja = os.path.join('graficos', f'caja_bigotes_{columna}.png')
                plt.savefig(ruta_graficos_caja)
                plt.close()
                resultados['grafico_caja'] = ruta_graficos_caja

                # Cálculo de probabilidades según distribuciones
                resultados['probabilidades'] = self.calcular_probabilidades(datos)

            else:
                # Frecuencias para variables categóricas
                frecuencias = datos.value_counts()
                resultados['frecuencias'] = frecuencias

                # Gráfico de barras
                plt.figure(figsize=(10, 6))
                frecuencias.plot(kind='bar', color='skyblue')
                plt.title(f'Frecuencias de {columna}')
                plt.xlabel(columna)
                plt.ylabel('Frecuencia')
                ruta_graficos_barras = os.path.join('graficos', f'frecuencias_{columna}.png')
                plt.savefig(ruta_graficos_barras)
                plt.close()
                resultados['grafico_barras'] = ruta_graficos_barras

            # Generar interpretación detallada
            resultados['interpretacion'] = self.generar_interpretacion(columna, resultados, datos)

            # Generar informe en PDF
            self.generar_informe_pdf(columna, resultados)

            return resultados
        except Exception as e:
            logging.exception(f"Error al analizar la variable '{columna}': {e}")
            raise e

    def generar_interpretacion(self, columna, resultados, datos):
        """
        Genera una interpretación detallada de los resultados.

        :param columna: Nombre de la columna analizada.
        :param resultados: Diccionario con los resultados del análisis.
        :param datos: Serie de pandas con los datos analizados.
        :return: Cadena con la interpretación de los resultados.
        """
        try:
            interpretacion = f"Análisis detallado de la variable '{columna}':\n\n"

            if 'media' in resultados:
                interpretacion += f"- **Media**: La media de {columna} es {resultados['media']:.2f}, lo que indica que, en promedio, los valores son {'altos' if resultados['media'] > datos.median() else 'bajos'}.\n"
                interpretacion += f"- **Mediana**: La mediana es {resultados['mediana']:.2f}, lo que significa que el 50% de los datos está por debajo de este valor.\n"
                interpretacion += f"- **Moda**: {resultados['moda']}, siendo el valor que más se repite en los datos.\n"
                interpretacion += f"- **Desviación Estándar**: {resultados['desv_std']:.2f}, indicando que los datos {'están dispersos' if resultados['desv_std'] > resultados['media']/2 else 'están concentrados'} alrededor de la media.\n"
                interpretacion += f"- **Coeficiente de Variación**: {resultados['coef_var']:.2f}%, lo que sugiere una {'alta' if resultados['coef_var'] > 30 else 'baja'} variabilidad relativa en los datos.\n\n"

                # Ejemplos de decisiones
                interpretacion += "Ejemplos de decisiones basadas en estos resultados:\n"
                interpretacion += "- Si la media de edad es alta, se podrían adquirir más libros para adultos.\n"
                interpretacion += "- Una alta desviación estándar indica diversidad en los datos, lo que podría requerir estrategias segmentadas.\n"

                # Interpretación de probabilidades
                probs = resultados.get('probabilidades', {})
                if probs:
                    interpretacion += "\n**Probabilidades según distribuciones:**\n"
                    if probs.get('binomial') is not None:
                        interpretacion += f"- **Binomial**: {probs['binomial']:.4f}. Puede ayudar a estimar la probabilidad de éxito en eventos binarios.\n"

                    if probs.get('poisson') is not None:
                        interpretacion += f"- **Poisson**: {probs['poisson']:.4f}. Útil para modelar eventos raros en un intervalo de tiempo.\n"

                    if probs.get('normal') is not None:
                        interpretacion += f"- **Normal**: {probs['normal']:.4f}. Indica la probabilidad de valores cercanos a la media.\n"

                    if probs.get('hipergeometrica') is not None:
                        interpretacion += f"- **Hipergeométrica**: {probs['hipergeometrica']:.4f}. Se aplica en muestreos sin reemplazo.\n"
            else:
                interpretacion += f"- **Moda**: La moda de {columna} es '{resultados['moda']}', siendo el valor más frecuente.\n"
                interpretacion += "Frecuencias de los diferentes valores:\n"
                for valor, frecuencia in resultados['frecuencias'].items():
                    interpretacion += f"    - {valor}: {frecuencia} veces\n"

                # Ejemplos de decisiones
                interpretacion += "\nEjemplos de decisiones basadas en estos resultados:\n"
                interpretacion += f"- Si '{resultados['moda']}' es el tipo de libro más prestado, se podrían adquirir más ejemplares de este.\n"

            return interpretacion
        except Exception as e:
            logging.exception(f"Error al generar la interpretación para '{columna}': {e}")
            return "No se pudo generar una interpretación detallada de los resultados."

    def generar_informe_pdf(self, columna, resultados):
        """
        Genera un informe en PDF con los resultados del análisis.

        :param columna: Nombre de la columna analizada.
        :param resultados: Diccionario con los resultados del análisis.
        """
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f'Informe de Análisis de {columna}', ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", '', 12)
            interpretacion = resultados.get('interpretacion', '')
            for line in interpretacion.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf.ln(10)

            # Agregar tablas de estadísticas
            if 'frecuencias' in resultados:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, 'Frecuencias:', ln=True)
                pdf.set_font("Arial", '', 12)
                frecuencias = resultados['frecuencias']
                for valor, frecuencia in frecuencias.items():
                    pdf.cell(0, 10, f"{valor}: {frecuencia} veces", ln=True)
                pdf.ln(5)
            else:
                # Mostrar otras estadísticas
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, 'Estadísticas:', ln=True)
                pdf.set_font("Arial", '', 12)
                stats = {k: v for k, v in resultados.items() if k not in ['interpretacion', 'probabilidades', 'frecuencias']}
                for clave, valor in stats.items():
                    pdf.cell(0, 10, f"{clave.replace('_', ' ').capitalize()}: {valor}", ln=True)
                pdf.ln(5)

            # Agregar probabilidades
            probs = resultados.get('probabilidades', {})
            if probs:
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, 'Probabilidades según distribuciones:', ln=True)
                pdf.set_font("Arial", '', 12)
                for dist, prob in probs.items():
                    if prob is not None:
                        pdf.cell(0, 10, f"{dist.capitalize()}: {prob:.4f}", ln=True)
                pdf.ln(5)

            # Agregar gráficos
            graficos = ['grafico_distribucion', 'grafico_caja', 'grafico_barras']
            for grafico in graficos:
                ruta = resultados.get(grafico)
                if ruta and os.path.exists(ruta):
                    pdf.image(ruta, x=10, w=pdf.w - 20)
                    pdf.ln(10)

            # Guardar el PDF
            ruta_carpeta = 'PDF'
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
            ruta_pdf = os.path.join(ruta_carpeta, f'Informe_{columna}.pdf')
            pdf.output(ruta_pdf)
            logging.info(f"Informe PDF generado en '{ruta_pdf}'.")
        except Exception as e:
            logging.exception(f"Error al generar el informe PDF para '{columna}': {e}")

    def calcular_probabilidades(self, datos):
        """
        Calcula probabilidades según diferentes distribuciones.

        :param datos: Serie de pandas con los datos.
        :return: Diccionario con las probabilidades calculadas.
        """
        try:
            probabilidades = {}
            probabilidades['binomial'] = self.calcular_probabilidad_binomial(datos)
            probabilidades['poisson'] = self.calcular_probabilidad_poisson(datos)
            probabilidades['normal'] = self.calcular_probabilidad_normal(datos)
            probabilidades['hipergeometrica'] = self.calcular_probabilidad_hipergeometrica(datos)
            return probabilidades
        except Exception as e:
            logging.exception(f"Error al calcular probabilidades: {e}")
            return None

    def calcular_probabilidad_binomial(self, datos):
        """
        Calcula la probabilidad binomial para los datos.

        :param datos: Serie de pandas con los datos numéricos.
        :return: Probabilidad binomial.
        """
        try:
            n = len(datos)
            p = datos.mean() / datos.max() if datos.max() != 0 else 0
            k = datos.sum()

            logging.debug(f"Calculando probabilidad binomial con n={n}, p={p}, k={k}")

            if not 0 <= p <= 1:
                logging.error("La probabilidad 'p' debe estar entre 0 y 1.")
                return None

            prob = stats.binom.pmf(k, n, p)
            return prob
        except ValueError as e:
            logging.error(f"Error al calcular probabilidad binomial: {e}")
            return None
        except Exception as e:
            logging.exception(f"Error inesperado al calcular probabilidad binomial: {e}")
            return None

    def calcular_probabilidad_poisson(self, datos):
        """
        Calcula la probabilidad Poisson para los datos.

        :param datos: Serie de pandas con los datos numéricos.
        :return: Probabilidad Poisson.
        """
        try:
            lambda_ = datos.mean()
            k = int(lambda_)
            logging.debug(f"Calculando probabilidad Poisson con λ={lambda_}, k={k}")
            prob = stats.poisson.pmf(k, lambda_)
            return prob
        except Exception as e:
            logging.exception(f"Error al calcular probabilidad Poisson: {e}")
            return None

    def calcular_probabilidad_normal(self, datos):
        """
        Calcula la probabilidad normal para los datos.

        :param datos: Serie de pandas con los datos numéricos.
        :return: Probabilidad normal.
        """
        try:
            mu = datos.mean()
            sigma = datos.std()
            logging.debug(f"Calculando probabilidad Normal con μ={mu}, σ={sigma}")
            prob = stats.norm.cdf(mu + sigma, mu, sigma) - stats.norm.cdf(mu - sigma, mu, sigma)
            return prob
        except Exception as e:
            logging.exception(f"Error al calcular probabilidad Normal: {e}")
            return None

    def calcular_probabilidad_hipergeometrica(self, datos):
        """
        Calcula la probabilidad hipergeométrica para los datos.

        :param datos: Serie de pandas con los datos numéricos.
        :return: Probabilidad hipergeométrica.
        """
        try:
            N = len(self.df)
            n = len(datos)
            K = int(datos.sum())
            k = int(datos.sum())
            logging.debug(f"Calculando probabilidad Hipergeométrica con N={N}, K={K}, n={n}, k={k}")
            prob = stats.hypergeom.pmf(k, N, K, n)
            return prob
        except Exception as e:
            logging.exception(f"Error al calcular probabilidad Hipergeométrica: {e}")
            return None