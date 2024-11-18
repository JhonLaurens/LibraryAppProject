# Archivo: modules/interfaz.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import pandas as pd
from modules.analisis import AnalisisEstadistico
from PIL import Image
import os
import logging

class InterfazUsuario:
    def __init__(self, app):
        self.app = app
        self.df = None
        self.sample = None
        self.analisis = None
        self.columnas_requeridas = [
            'ITEM', 'DOCUMENTO', 'NOMBRE', 'EDAD', 'GENERO',
            'ESTRATO', 'TIPO LIBROS', 'TIPO USUARIO', 'SEDE',
            'TIEMPO DE PRESTAMO'
        ]
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Configuración del layout responsivo
        self.frame_principal = ctk.CTkFrame(self.app)
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=3)
        self.frame_principal.rowconfigure(1, weight=1)

        # Barra superior
        self.barra_superior = ctk.CTkFrame(self.frame_principal)
        self.barra_superior.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.titulo = ctk.CTkLabel(self.barra_superior, text="Análisis Estadístico de Biblioteca", font=ctk.CTkFont(size=24, weight="bold"))
        self.titulo.pack(side="left", padx=10, pady=10)

        self.btn_cerrar = ctk.CTkButton(self.barra_superior, text="×", width=40, command=self.app.quit)
        self.btn_cerrar.pack(side="right", padx=10, pady=10)

        # Panel de control
        self.panel_control = ctk.CTkFrame(self.frame_principal)
        self.panel_control.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Sección de carga
        self.btn_cargar = ctk.CTkButton(self.panel_control, text="Cargar Archivo Excel", command=self.cargar_archivo)
        self.btn_cargar.pack(fill="x", pady=5)

        # Sección de muestreo
        self.entrada_tamanio = ctk.CTkEntry(self.panel_control, placeholder_text="Tamaño de muestra")
        self.entrada_tamanio.pack(fill="x", pady=5)

        self.btn_muestreo_simple = ctk.CTkButton(self.panel_control, text="Muestreo Aleatorio Simple", command=lambda: self.crear_muestra("simple"))
        self.btn_muestreo_simple.pack(fill="x", pady=5)

        # Sección de análisis
        self.variable_seleccionada = ctk.CTkOptionMenu(self.panel_control, values=self.columnas_requeridas)
        self.variable_seleccionada.pack(fill="x", pady=5)

        self.btn_analizar = ctk.CTkButton(self.panel_control, text="Analizar Variable", command=self.analizar_variable)
        self.btn_analizar.pack(fill="x", pady=5)

        # Nuevas funcionalidades para probabilidad
        self.lbl_probabilidad = ctk.CTkLabel(self.panel_control, text="Análisis de Probabilidad")
        self.lbl_probabilidad.pack(pady=10)

        self.variable_prob1 = ctk.CTkOptionMenu(self.panel_control, values=self.columnas_requeridas)
        self.variable_prob1.pack(fill="x", pady=5)

        self.variable_prob2 = ctk.CTkOptionMenu(self.panel_control, values=self.columnas_requeridas)
        self.variable_prob2.pack(fill="x", pady=5)

        self.btn_probabilidad_conjunta = ctk.CTkButton(self.panel_control, text="Probabilidad Conjunta", command=self.calcular_probabilidad_conjunta)
        self.btn_probabilidad_conjunta.pack(fill="x", pady=5)

        self.btn_probabilidad_condicional = ctk.CTkButton(self.panel_control, text="Probabilidad Condicional", command=self.calcular_probabilidad_condicional)
        self.btn_probabilidad_condicional.pack(fill="x", pady=5)

        # Botón para mostrar datos
        self.btn_mostrar_datos = ctk.CTkButton(self.panel_control, text="Mostrar Datos", command=self.mostrar_datos)
        self.btn_mostrar_datos.pack(fill="x", pady=5)

        # Panel de resultados
        self.panel_resultados = ctk.CTkFrame(self.frame_principal)
        self.panel_resultados.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Área de resultados
        self.area_resultados = ctk.CTkTextbox(self.panel_resultados)
        self.area_resultados.pack(fill="both", expand=True)

        # Botón para descargar gráfico
        self.btn_descargar = ctk.CTkButton(self.panel_resultados, text="Descargar Gráfico", command=self.descargar_grafico)
        self.btn_descargar.pack(pady=5)

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xls")])
        if archivo:
            threading.Thread(target=self.procesar_archivo, args=(archivo,)).start()

    def procesar_archivo(self, archivo):
        try:
            self.df = pd.read_excel(archivo)
            if all(col in self.df.columns for col in self.columnas_requeridas):
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
                self.analisis = AnalisisEstadistico(self.df)
            else:
                missing_cols = set(self.columnas_requeridas) - set(self.df.columns)
                messagebox.showerror("Error", f"Faltan las siguientes columnas: {', '.join(missing_cols)}")
        except Exception as e:
            logging.exception("Error al procesar el archivo")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def crear_muestra(self, metodo):
        if self.df is not None:
            try:
                tamanio = int(self.entrada_tamanio.get())
                if metodo == "simple":
                    self.sample = self.df.sample(n=tamanio)
                    messagebox.showinfo("Éxito", "Muestra creada correctamente.")
                elif metodo == "estratificado":
                    self.sample = self.muestreo_estratificado(tamanio)
                    messagebox.showinfo("Éxito", f"Muestra de {len(self.sample)} registros creada exitosamente")
            except ValueError as e:
                logging.exception("Error en el tamaño de la muestra")
                messagebox.showerror("Error", "Ingrese un tamaño de muestra válido.")
            except Exception as e:
                logging.exception("Error al crear la muestra")
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
        else:
            messagebox.showerror("Error", "Primero cargue un archivo.")

    def muestreo_estratificado(self, tamanio):
        try:
            estratos = self.df['ESTRATO'].unique()
            proporciones = self.df['ESTRATO'].value_counts(normalize=True)
            tamanio_estrato = (proporciones * tamanio).round().astype(int)
            muestras = [self.df[self.df['ESTRATO'] == estrato].sample(n=tamano, random_state=1)
                        for estrato, tamano in tamanio_estrato.items()]
            muestra = pd.concat(muestras).reset_index(drop=True)
            return muestra
        except Exception as e:
            logging.exception("Error en muestreo estratificado")
            messagebox.showerror("Error", f"Error en muestreo estratificado: {str(e)}")
            return None

    def analizar_variable(self):
        if self.sample is not None:
            try:
                columna = self.variable_seleccionada.get()
                resultados = self.analisis.analizar_variable(self.sample, columna)
                self.mostrar_resultados(resultados, columna)
            except Exception as e:
                logging.exception("Error al analizar la variable")
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
        else:
            messagebox.showerror("Error", "Primero cree una muestra.")

    def calcular_probabilidad_conjunta(self):
        if self.df is not None:
            try:
                col1 = self.variable_prob1.get()
                col2 = self.variable_prob2.get()
                conjunta = self.analisis.calcular_probabilidad_conjunta(col1, col2)
                self.mostrar_probabilidad_conjunta(conjunta, col1, col2)
            except Exception as e:
                logging.exception("Error al calcular probabilidad conjunta")
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
        else:
            messagebox.showerror("Error", "Primero cargue un archivo.")

    def calcular_probabilidad_condicional(self):
        if self.df is not None:
            try:
                evento = self.variable_prob1.get()
                condicion = self.variable_prob2.get()
                condicional = self.analisis.calcular_probabilidad_condicional(evento, condicion)
                self.mostrar_probabilidad_condicional(condicional, evento, condicion)
            except Exception as e:
                logging.exception("Error al calcular probabilidad condicional")
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
        else:
            messagebox.showerror("Error", "Primero cargue un archivo.")

    def mostrar_resultados(self, resultados, columna):
        self.area_resultados.delete("1.0", "end")
        self.area_resultados.insert("end", f"Resultados del análisis de {columna}:\n\n")
        for key, value in resultados.items():
            if isinstance(value, pd.Series):
                self.area_resultados.insert("end", f"{key}:\n{value.to_string()}\n\n")
            else:
                self.area_resultados.insert("end", f"{key}: {value}\n\n")

        # Limpiar gráficos anteriores
        for widget in self.panel_resultados.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and hasattr(widget, 'image'):
                widget.destroy()

        # Mostrar gráficos
        if pd.api.types.is_numeric_dtype(self.sample[columna]):
            grafico_normal_path = 'grafico_normal.png'
            grafico_caja_path = 'grafico_caja.png'
            if os.path.exists(grafico_normal_path) and os.path.exists(grafico_caja_path):
                imagen_normal = ctk.CTkImage(light_image=Image.open(grafico_normal_path), size=(400, 300))
                imagen_caja = ctk.CTkImage(light_image=Image.open(grafico_caja_path), size=(400, 300))

                label_imagen_normal = ctk.CTkLabel(self.panel_resultados, image=imagen_normal, text="")
                label_imagen_normal.image = imagen_normal  # Mantener referencia
                label_imagen_normal.pack(pady=5)

                label_imagen_caja = ctk.CTkLabel(self.panel_resultados, image=imagen_caja, text="")
                label_imagen_caja.image = imagen_caja  # Mantener referencia
                label_imagen_caja.pack(pady=5)
            else:
                self.area_resultados.insert("end", "No se pudieron cargar los gráficos.\n")
        else:
            grafico_barras_path = 'grafico_barras.png'
            if os.path.exists(grafico_barras_path):
                imagen_barras = ctk.CTkImage(light_image=Image.open(grafico_barras_path), size=(400, 300))
                label_imagen_barras = ctk.CTkLabel(self.panel_resultados, image=imagen_barras, text="")
                label_imagen_barras.image = imagen_barras  # Mantener referencia
                label_imagen_barras.pack(pady=5)
            else:
                self.area_resultados.insert("end", "No se pudo cargar el gráfico de barras.\n")

        # Guardar gráfico actual para descarga
        self.guardar_grafico_actual()

        # Mostrar interpretación
        interpretacion = self.obtener_interpretacion(columna, resultados)
        self.area_resultados.insert("end", f"Interpretación:\n{interpretacion}\n")

    def mostrar_probabilidad_conjunta(self, conjunta, col1, col2):
        self.area_resultados.delete("1.0", "end")
        self.area_resultados.insert("end", f"Probabilidad Conjunta entre {col1} y {col2}:\n\n")
        self.area_resultados.insert("end", conjunta.to_string())
        # Opcional: Mostrar gráfico de mapa de calor
        plt.figure(figsize=(10, 6))
        sns.heatmap(conjunta, annot=True, cmap='Blues')
        plt.title(f'Probabilidad Conjunta de {col1} y {col2}')
        plt.savefig('grafico_conjunta.png')
        plt.close()
        if os.path.exists('grafico_conjunta.png'):
            imagen_conjunta = ctk.CTkImage(light_image=Image.open('grafico_conjunta.png'), size=(400, 300))
            label_imagen_conjunta = ctk.CTkLabel(self.panel_resultados, image=imagen_conjunta, text="")
            label_imagen_conjunta.image = imagen_conjunta
            label_imagen_conjunta.pack(pady=5)

    def mostrar_probabilidad_condicional(self, condicional, evento, condicion):
        self.area_resultados.delete("1.0", "end")
        self.area_resultados.insert("end", f"Probabilidad Condicional de {evento} dado {condicion}:\n\n")
        self.area_resultados.insert("end", condicional.to_string())
        # Opcional: Mostrar gráfico de mapa de calor
        plt.figure(figsize=(10, 6))
        sns.heatmap(condicional, annot=True, cmap='Greens')
        plt.title(f'Probabilidad Condicional de {evento} dado {condicion}')
        plt.savefig('grafico_condicional.png')
        plt.close()
        if os.path.exists('grafico_condicional.png'):
            imagen_condicional = ctk.CTkImage(light_image=Image.open('grafico_condicional.png'), size=(400, 300))
            label_imagen_condicional = ctk.CTkLabel(self.panel_resultados, image=imagen_condicional, text="")
            label_imagen_condicional.image = imagen_condicional
            label_imagen_condicional.pack(pady=5)

    def guardar_grafico_actual(self):
        try:
            fig = plt.gcf()
            fig.savefig('grafico_actual.png')
        except Exception as e:
            logging.exception("Error al guardar el gráfico actual")
            messagebox.showerror("Error", f"Ocurrió un error al guardar el gráfico: {e}")

    def obtener_interpretacion(self, columna, resultados):
        try:
            interpretacion = self.interpretaciones.get(columna, "No hay interpretación disponible para esta columna.")
            return interpretacion
        except Exception as e:
            logging.exception("Error al obtener interpretación")
            return "Error al obtener interpretación."

    def mostrar_interpretacion(self, columna):
        interpretacion = self.interpretaciones.get(columna, "No hay interpretación disponible para esta columna.")
        alert = ctk.CTkFrame(self.panel_resultados, fg_color="#FFF4E5", corner_radius=10)
        alert.pack(fill="x", padx=20, pady=10)
        label_interpretacion = ctk.CTkLabel(alert, text=interpretacion, justify="left", wraplength=800, font=ctk.CTkFont(size=14))
        label_interpretacion.pack(pady=10, padx=20)

    def limpiar_resultados(self):
        for widget in self.panel_resultados.winfo_children():
            widget.destroy()
        self.area_resultados.delete("1.0", "end")
        plt.close('all')

    def descargar_grafico(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf")])
        if ruta:
            try:
                if os.path.exists('grafico_actual.png'):
                    img = Image.open('grafico_actual.png')
                    img.save(ruta)
                    messagebox.showinfo("Éxito", "Gráfico descargado correctamente.")
                else:
                    messagebox.showerror("Error", "El archivo 'grafico_actual.png' no existe.")
            except Exception as e:
                logging.exception("Error al descargar el gráfico")
                messagebox.showerror("Error", f"No se pudo descargar el gráfico: {e}")

    def mostrar_datos(self):
        if self.sample is not None:
            top = ctk.CTkToplevel(self.app)
            top.title("Datos de la Muestra")
            top.geometry("800x600")

            tree = ttk.Treeview(top)
            tree.pack(fill="both", expand=True)

            tree["columns"] = list(self.sample.columns)
            tree["show"] = "headings"

            for col in self.sample.columns:
                tree.heading(col, text=col)

            for index, row in self.sample.iterrows():
                tree.insert("", "end", values=list(row))
        else:
            messagebox.showerror("Error", "No hay datos para mostrar.")

    def ejecutar(self):
        self.app.mainloop()