import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from tkinter import filedialog, messagebox, ttk
import scipy.stats as stats

class AppAnalisisEstadistico:
    def __init__(self, tema="azul"):
        self.app = ctk.CTk()
        self.app.title("Análisis Estadístico de Biblioteca")
        self.app.geometry("1280x800")
        self.df = None
        self.sample = None
        self.columnas_requeridas = [
            'ITEM', 'DOCUMENTO', 'NOMBRE', 'EDAD', 'GENERO',
            'ESTRATO', 'TIPO LIBROS', 'TIPO USUARIO', 'SEDE',
            'TIEMPO DE PRESTAMO'
        ]
        self.interpretaciones = {  # Interpretaciones mejoradas
            'GENERO': """Interpretación del Análisis de Género:
            Este gráfico muestra la distribución de géneros entre los usuarios. Observa si hay una diferencia significativa entre géneros.  Una distribución desigual podría sugerir sesgos de acceso o uso de la biblioteca.  Considera factores externos que podrían influir en esta distribución.""",
            'ESTRATO': """Interpretación del Análisis de Estratos Socioeconómicos:
            Este gráfico representa la distribución de los usuarios según su estrato socioeconómico. Analiza si hay una concentración en ciertos estratos, lo que podría indicar que la biblioteca atiende principalmente a un grupo socioeconómico específico. Una distribución más equilibrada indicaría una mayor equidad de acceso.  Considera si la muestra es representativa de la población.""",
            'EDAD': """Interpretación del Análisis de Edad:
            El histograma muestra la distribución de las edades de los usuarios. Observa la media, la mediana, la moda y la desviación estándar.  Considera si la distribución es simétrica o sesgada, y si hay valores atípicos (outliers) que podrían indicar un grupo de usuarios con características particulares.  Considera el contexto para interpretar estos resultados.""",
            'TIEMPO DE PRESTAMO': """Interpretación del Análisis de Tiempo de Préstamo:
            Este gráfico ilustra la duración de los préstamos. Analiza la media, la mediana y la moda para entender la duración típica. Considera la desviación estándar, que indica la variabilidad en la duración de los préstamos. Valores atípicos pueden indicar usuarios o tipos de materiales con patrones de préstamo inusuales.  Compara estos resultados con las políticas de préstamo de la biblioteca."""
        }
        self.configurar_tema(tema)
        self.configurar_interfaz()

    def configurar_tema(self, tema):
        temas = {
            "azul": {"modo": "light", "color": "blue", "fondo": "#F5F5F5"},
            "verde": {"modo": "light", "color": "green", "fondo": "#F0F4F0"},
            "oscuro": {"modo": "dark", "color": "blue", "fondo": "#2B2B2B"}
        }
        tema_config = temas.get(tema, temas["azul"])
        ctk.set_appearance_mode(tema_config["modo"])
        ctk.set_default_color_theme(tema_config["color"])
        self.app.configure(fg_color=tema_config["fondo"])

    def configurar_interfaz(self):
        self.panel_principal = ctk.CTkFrame(self.app, fg_color="transparent")
        self.panel_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        self.panel_control = ctk.CTkFrame(self.panel_principal)
        self.panel_control.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.panel_resultados = ctk.CTkFrame(self.panel_principal)
        self.panel_resultados.grid(row=0, column=1, sticky="nsew")

        self.panel_principal.grid_columnconfigure(1, weight=3)
        self.panel_principal.grid_rowconfigure(0, weight=1)

        self.configurar_panel_control()
        self.configurar_panel_resultados()

    def configurar_panel_control(self):
        titulo = ctk.CTkLabel(self.panel_control, text="Panel de Control", font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(pady=20)

        self.boton_cargar = ctk.CTkButton(self.panel_control, text="Cargar Archivo Excel", command=self.cargar_archivo, height=40)
        self.boton_cargar.pack(pady=20, padx=20, fill="x")

        separador = ctk.CTkFrame(self.panel_control, height=2)
        separador.pack(fill="x", pady=10, padx=20)

        self.configurar_panel_muestreo()

        separador2 = ctk.CTkFrame(self.panel_control, height=2)
        separador2.pack(fill="x", pady=10, padx=20)

        self.configurar_panel_analisis()

    def configurar_panel_muestreo(self):
        frame_muestreo = ctk.CTkFrame(self.panel_control)
        frame_muestreo.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_muestreo, text="Método de Muestreo", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        frame_tamanio = ctk.CTkFrame(frame_muestreo)
        frame_tamanio.pack(fill="x", pady=5)

        ctk.CTkLabel(frame_tamanio, text="Tamaño de muestra:").pack(side="left", padx=5)
        self.entrada_tamanio = ctk.CTkEntry(frame_tamanio, width=80)
        self.entrada_tamanio.pack(side="left", padx=5)
        self.entrada_tamanio.insert(0, "30")

        self.boton_simple = ctk.CTkButton(frame_muestreo, text="Muestreo Aleatorio Simple", command=lambda: self.crear_muestra("simple"))
        self.boton_simple.pack(pady=5, fill="x")

        self.boton_estratificado = ctk.CTkButton(frame_muestreo, text="Muestreo Estratificado", command=lambda: self.crear_muestra("estratificado"))
        self.boton_estratificado.pack(pady=5, fill="x")


    def configurar_panel_analisis(self):
        frame_analisis = ctk.CTkFrame(self.panel_control)
        frame_analisis.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_analisis, text="Análisis", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        self.botones_analisis = {}
        for col in ['GENERO', 'ESTRATO', 'EDAD', 'TIEMPO DE PRESTAMO']:
            self.botones_analisis[col] = self.crear_boton_analisis(
                frame_analisis, f"Análisis de {col}", lambda c=col: self.analizar(c)
            )


    def configurar_panel_resultados(self):
        self.canvas_resultados = ctk.CTkScrollableFrame(self.panel_resultados, label_text="Resultados del Análisis", label_font=ctk.CTkFont(size=20, weight="bold"))
        self.canvas_resultados.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_boton_analisis(self, parent, texto, comando):
        boton = ctk.CTkButton(parent, text=texto, command=comando, state="disabled", height=35)
        boton.pack(pady=5, fill="x")
        return boton

    def habilitar_botones_analisis(self):
        for boton in self.botones_analisis.values():
            boton.configure(state="normal")

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])
        if archivo:
            try:
                self.df = pd.read_excel(archivo)
                if all(col in self.df.columns for col in self.columnas_requeridas):
                    messagebox.showinfo("Éxito", f"Archivo cargado correctamente. {len(self.df)} registros encontrados.")
                    self.habilitar_botones_analisis()
                else:
                    missing_cols = set(self.columnas_requeridas) - set(self.df.columns)
                    messagebox.showerror("Error", f"Faltan las siguientes columnas: {', '.join(missing_cols)}")
            except FileNotFoundError:
                messagebox.showerror("Error", "Archivo no encontrado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def crear_muestra(self, metodo):
        if self.df is None:
            messagebox.showerror("Error", "Primero debe cargar un archivo de datos")
            return

        try:
            tamanio = int(self.entrada_tamanio.get())
            if tamanio <= 0 or tamanio > len(self.df):
                raise ValueError("Tamaño de muestra inválido. Debe ser un número positivo menor o igual al tamaño del conjunto de datos.")

            if metodo == "simple":
                self.sample = self.df.sample(n=tamanio)
            elif metodo == "estratificado":
                proporciones = self.df['ESTRATO'].value_counts(normalize=True)
                sizes = [int(round(p * tamanio)) for p in proporciones]
                self.sample = self.df.groupby('ESTRATO', group_keys=False).apply(lambda x: x.sample(n=sizes[proporciones.index.get_loc(x.name)] if len(x) >= sizes[proporciones.index.get_loc(x.name)] else len(x)))
                self.sample = self.sample.sample(n=tamanio) # Ensure sample size

            messagebox.showinfo("Éxito", f"Muestra de {len(self.sample)} registros creada exitosamente")

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except KeyError:
            messagebox.showerror("Error", "La columna 'ESTRATO' no se encuentra en el archivo.  Asegúrate de que la columna 'ESTRATO' exista en tu archivo Excel.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la muestra: {str(e)}")


    def limpiar_resultados(self):
        for widget in self.canvas_resultados.winfo_children():
            widget.destroy()
        plt.close('all')

    def analizar(self, columna):
        if self.sample is None:
            messagebox.showerror("Error", "Primero debe crear una muestra")
            return

        self.limpiar_resultados()

        if pd.api.types.is_numeric_dtype(self.sample[columna]):
            self.analizar_numerico(columna)
        else:
            self.analizar_categorico(columna)

    def analizar_categorico(self, columna):
        freq = self.sample[columna].value_counts()
        moda = self.sample[columna].mode().iloc[0] if not self.sample[columna].empty else "No data"

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        sns.barplot(x=freq.index, y=freq.values, ax=ax1, palette="viridis")
        ax1.set_title(f'Diagrama de Barras ({columna})', fontsize=14)
        ax1.tick_params(axis='x', rotation=45)
        ax1.set_ylabel('Frecuencia')
        ax1.set_xlabel(columna)

        ax2.pie(freq.values, labels=freq.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
        ax2.set_title(f'Distribución Porcentual ({columna})', fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_resultados)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        self.mostrar_estadisticas_e_interpretaciones(columna, freq, moda)

    def analizar_numerico(self, columna):
        datos = self.sample[columna]
        media = datos.mean()
        mediana = datos.median()
        moda = datos.mode().iloc[0] if not datos.empty else "No data"
        desv_std = datos.std()
        varianza = datos.var()
        coef_var = (desv_std / media) * 100 if media != 0 else 0

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        sns.histplot(data=datos, kde=True, ax=ax1, color="skyblue")
        ax1.set_title(f'Histograma ({columna})', fontsize=14)
        ax1.set_xlabel(columna)
        ax1.set_ylabel('Frecuencia')

        sorted_data = np.sort(datos)
        cumfreq = np.arange(1, len(datos) + 1) / len(datos) if not datos.empty else []
        ax2.plot(sorted_data, cumfreq, marker='o', color="coral")
        ax2.set_title(f'Ojiva ({columna})', fontsize=14)
        ax2.set_xlabel(columna)
        ax2.set_ylabel('Frecuencia Acumulada')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_resultados)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        self.mostrar_estadisticas_e_interpretaciones(columna, None, moda, media, mediana, desv_std, varianza, coef_var)

    def mostrar_estadisticas_e_interpretaciones(self, columna, freq=None, moda=None, media=None, mediana=None, desv_std=None, varianza=None, coef_var=None):
        stats_text = f"Estadísticas para {columna}:\n"
        if freq is not None:
            stats_text += f"- Moda: {moda}\n- Frecuencias:\n{freq.to_string()}\n"
        else:
            stats_text += f"- Media: {media:.2f}\n- Mediana: {mediana:.2f}\n- Moda: {moda:.2f}\n- Desviación Estándar: {desv_std:.2f}\n- Varianza: {varianza:.2f}\n- Coeficiente de Variación: {coef_var:.2f}%\n"

        self.mostrar_texto_resultados(stats_text)
        self.mostrar_interpretacion(columna)

    def mostrar_texto_resultados(self, texto):
        label = ctk.CTkLabel(self.canvas_resultados, text=texto, justify="left", font=ctk.CTkFont(family="Courier", size=12), wraplength=600)
        label.pack(pady=10, padx=20)

    def mostrar_interpretacion(self, columna):
        interpretacion = self.interpretaciones.get(columna, "No hay interpretación disponible para esta columna.")
        label_interpretacion = ctk.CTkLabel(self.canvas_resultados, text=interpretacion, justify="left", wraplength=600, font=ctk.CTkFont(size=14))
        label_interpretacion.pack(pady=10, padx=20)

    def ejecutar(self):
        self.app.mainloop()

def main():
    app = AppAnalisisEstadistico(tema="verde")
    app.ejecutar()

if __name__ == "__main__":
    main()