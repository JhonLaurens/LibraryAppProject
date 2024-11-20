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
    """
    Clase que maneja la interfaz gráfica de usuario de la aplicación.
    """

    def __init__(self, app):
        """
        Inicializa la interfaz de usuario.

        :param app: Instancia de la aplicación de tkinter.
        """
        self.app = app
        self.df = None
        self.sample = None
        self.analisis = None
        self.resultados = {}
        self.columna_actual = None
        self.columnas_requeridas = [
            'ITEM', 'DOCUMENTO', 'NOMBRE', 'EDAD', 'GENERO',
            'ESTRATO', 'TIPO LIBROS', 'TIPO USUARIO', 'SEDE',
            'TIEMPO DE PRESTAMO'
        ]
        self.configurar_interfaz()

    def configurar_interfaz(self):
        """
        Configura todos los componentes de la interfaz gráfica.
        """
        # Configurar el tema y los colores
        ctk.set_appearance_mode("Light")  # Cambiado a "Light" para mayor claridad
        ctk.set_default_color_theme("blue")  # Tema de color azul

        # Configuración del layout responsivo
        self.frame_principal = ctk.CTkFrame(
            self.app, fg_color="#F0F0F0", corner_radius=10, border_width=2, border_color="#CCCCCC"
        )
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=3)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=0)  # Ajustado para el logo

        # Barra superior
        self.barra_superior = ctk.CTkFrame(self.frame_principal, fg_color="#E0E0E0", corner_radius=10)
        self.barra_superior.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.barra_superior.grid_columnconfigure(0, weight=1)
        self.barra_superior.grid_columnconfigure(1, weight=0)

        self.titulo = ctk.CTkLabel(
            self.barra_superior,
            text="Proyecto Final Estadística Librería Analítica",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#333333"
        )
        self.titulo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.btn_cerrar = ctk.CTkButton(
            self.barra_superior,
            text="×",
            width=40,
            fg_color="#FF5555",
            hover_color="#FF4444",
            command=self.app.quit
        )
        self.btn_cerrar.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Panel de control
        self.panel_control = ctk.CTkFrame(
            self.frame_principal, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#DDDDDD"
        )
        self.panel_control.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Sección de carga de archivo
        self.btn_cargar = ctk.CTkButton(
            self.panel_control,
            text="📂 Cargar Archivo Excel",
            command=self.cargar_archivo,
            fg_color="#4CAF50",
            hover_color="#45A049",
            corner_radius=8
        )
        self.btn_cargar.pack(fill="x", pady=10, padx=20)

        # Sección de muestreo
        self.entrada_tamanio = ctk.CTkEntry(
            self.panel_control,
            placeholder_text="📊 Tamaño de muestra",
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            text_color="#333333",
            border_width=1,
            corner_radius=8
        )
        self.entrada_tamanio.pack(fill="x", pady=5, padx=20)

        self.btn_muestreo_simple = ctk.CTkButton(
            self.panel_control,
            text="🔀 Muestreo Aleatorio Simple",
            command=lambda: self.crear_muestra("simple"),
            fg_color="#2196F3",
            hover_color="#1E88E5",
            corner_radius=8
        )
        self.btn_muestreo_simple.pack(fill="x", pady=10, padx=20)

        # Sección de análisis
        self.variable_seleccionada = ctk.CTkOptionMenu(
            self.panel_control,
            values=self.columnas_requeridas,
            dropdown_fg_color="#F0F0F0",
            dropdown_hover_color="#E0E0E0",
            button_color="#555555",
            button_hover_color="#666666",
            text_color="#333333",
            corner_radius=8
        )
        self.variable_seleccionada.pack(fill="x", pady=5, padx=20)

        self.btn_analizar = ctk.CTkButton(
            self.panel_control,
            text="📈 Analizar Variable",
            command=self.analizar_variable,
            fg_color="#FF9800",
            hover_color="#FB8C00",
            corner_radius=8
        )
        self.btn_analizar.pack(fill="x", pady=10, padx=20)

        # Opciones de visualización
        self.tipo_visualizacion = ctk.CTkOptionMenu(
            self.panel_control,
            values=["Tabla 📊", "Gráfico 📈", "Ambos 🧩"],
            dropdown_fg_color="#F0F0F0",
            dropdown_hover_color="#E0E0E0",
            button_color="#555555",
            button_hover_color="#666666",
            text_color="#333333",
            corner_radius=8
        )
        self.tipo_visualizacion.set("Ambos 🧩")
        self.tipo_visualizacion.pack(fill="x", pady=5, padx=20)

        # Botón para mostrar datos
        self.btn_mostrar_datos = ctk.CTkButton(
            self.panel_control,
            text="👁‍🗨 Mostrar Datos",
            command=self.mostrar_datos,
            fg_color="#9C27B0",
            hover_color="#8E24AA",
            corner_radius=8
        )
        self.btn_mostrar_datos.pack(fill="x", pady=10, padx=20)

        # Botón para generar PDF
        self.btn_generar_pdf = ctk.CTkButton(
            self.panel_control,
            text="📄 Generar Informe PDF",
            command=self.generar_pdf,
            fg_color="#FF5722",
            hover_color="#E64A19",
            corner_radius=8
        )
        self.btn_generar_pdf.pack(fill="x", pady=10, padx=20)

        # Panel de logo debajo del botón 'Generar PDF'
        self.panel_logo = ctk.CTkFrame(
            self.panel_control, 
            fg_color="#FFFFFF", 
            corner_radius=10, 
            border_width=1, 
            border_color="#DDDDDD"
        )
        self.panel_logo.pack(fill="x", pady=10, padx=20)

        # Cargar el logo.png (recomiendo usar .png en lugar de .ico)
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subir un nivel desde 'modules/'
        logo_path = os.path.join(script_dir, "images", "logo.png")  # Cambiar a .png

        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                img = img.resize((100, 100), Image.LANCZOS)  # Ajustar tamaño según necesidad
                logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
                self.label_logo = ctk.CTkLabel(self.panel_logo, image=logo_image, text="", corner_radius=10)
                self.label_logo.image = logo_image  # Mantener referencia
                self.label_logo.pack(pady=10)
            except Exception as e:
                logging.exception(f"Error al cargar el logo: {e}")
                self.label_logo = ctk.CTkLabel(self.panel_logo, text="Logo no encontrado", text_color="#FF0000")
                self.label_logo.pack(pady=10)
        else:
            logging.error(f"Logo no encontrado en '{logo_path}'")
            self.label_logo = ctk.CTkLabel(self.panel_logo, text="Logo no encontrado", text_color="#FF0000")
            self.label_logo.pack(pady=10)

        # Panel de resultados
        self.panel_resultados = ctk.CTkFrame(
            self.frame_principal, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#DDDDDD"
        )
        self.panel_resultados.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Área de resultados
        self.area_resultados = ctk.CTkTextbox(
            self.panel_resultados, 
            bg_color="#F9F9F9", 
            fg_color="#FFFFFF", 
            text_color="#333333",
            border_width=1,
            corner_radius=8
        )
        self.area_resultados.pack(fill="both", expand=True, padx=20, pady=20)

        # Canvas para mostrar gráficos
        self.canvas_graficos = ctk.CTkCanvas(
            self.panel_resultados, 
            bg="#F9F9F9", 
            highlightthickness=0
        )
        self.canvas_graficos.pack(fill="both", expand=True, padx=20, pady=20)

    def cargar_archivo(self):
        """
        Abre un cuadro de diálogo para seleccionar el archivo Excel a cargar.
        """
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if archivo:
            threading.Thread(target=self.procesar_archivo, args=(archivo,)).start()

    def procesar_archivo(self, archivo):
        """
        Procesa el archivo Excel seleccionado.

        :param archivo: Ruta del archivo Excel.
        """
        try:
            self.df = pd.read_excel(archivo)
            if all(col in self.df.columns for col in self.columnas_requeridas):
                messagebox.showinfo("🎉 Éxito", "Archivo cargado correctamente.")
                self.analisis = AnalisisEstadistico(self.df)
                logging.info(f"Archivo '{archivo}' cargado correctamente.")
            else:
                missing_cols = set(self.columnas_requeridas) - set(self.df.columns)
                messagebox.showerror(
                    "❌ Error",
                    f"Faltan las siguientes columnas: {', '.join(missing_cols)}"
                )
                logging.error(f"Faltan columnas: {', '.join(missing_cols)}")
        except Exception as e:
            logging.exception(f"Error al procesar el archivo: {e}")
            messagebox.showerror("❌ Error", f"Ocurrió un error: {e}")

    def crear_muestra(self, metodo):
        """
        Crea una muestra a partir del DataFrame cargado.

        :param metodo: Método de muestreo a utilizar ("simple" o "estratificado").
        """
        if self.df is not None:
            try:
                tamanio_texto = self.entrada_tamanio.get()
                if not tamanio_texto.isdigit():
                    raise ValueError("El tamaño de la muestra debe ser un número entero.")
                tamanio = int(tamanio_texto)
                if tamanio <= 0 or tamanio > len(self.df):
                    messagebox.showerror("❌ Error", "El tamaño de la muestra debe ser mayor que 0 y menor o igual al tamaño del conjunto de datos.")
                    logging.warning("Tamaño de muestra inválido.")
                    return
                if metodo == "simple":
                    self.sample = self.df.sample(n=tamanio, random_state=42)  # Añadido random_state para reproducibilidad
                    messagebox.showinfo("✅ Éxito", "Muestra creada correctamente.")
                    logging.info(f"Muestra aleatoria simple creada con tamaño {tamanio}.")
                # Se puede agregar lógica para otros métodos de muestreo
            except ValueError as ve:
                logging.exception("Error en el tamaño de la muestra.")
                messagebox.showerror("❌ Error", f"Ingrese un tamaño de muestra válido:\n{ve}")
            except Exception as e:
                logging.exception(f"Error al crear la muestra: {e}")
                messagebox.showerror("❌ Error", f"Ocurrió un error: {e}")
        else:
            messagebox.showerror("❌ Error", "Primero cargue un archivo.")
            logging.warning("Intento de crear muestra sin cargar archivo.")

    def analizar_variable(self):
        """
        Analiza la variable seleccionada y muestra los resultados según la opción elegida.
        """
        if self.sample is not None:
            try:
                columna = self.variable_seleccionada.get()
                if not columna:
                    messagebox.showerror("❌ Error", "Por favor, seleccione una variable para analizar.")
                    return
                self.columna_actual = columna
                resultados = self.analisis.analizar_variable(self.sample, columna)
                self.resultados = resultados
                self.mostrar_resultados(resultados, columna)
                logging.info(f"Variable '{columna}' analizada correctamente.")
            except Exception as e:
                logging.exception(f"Error al analizar la variable '{columna}': {e}")
                messagebox.showerror("❌ Error", f"Ocurrió un error al analizar la variable '{columna}': {e}")
        else:
            messagebox.showerror("❌ Error", "Primero cree una muestra.")
            logging.warning("Intento de análisis sin crear muestra.")

    def mostrar_resultados(self, resultados, columna):
        """
        Muestra los resultados del análisis en la interfaz.

        :param resultados: Diccionario con los resultados del análisis.
        :param columna: Nombre de la columna analizada.
        """
        self.area_resultados.delete("1.0", "end")
        self.area_resultados.insert("end", f"📊 Resultados del análisis de '{columna}':\n\n")

        # Mostrar interpretación
        if 'interpretacion' in resultados:
            self.area_resultados.insert("end", resultados['interpretacion'])
            self.area_resultados.insert("end", "\n\n")
        else:
            self.area_resultados.insert("end", "❓ No se pudo generar la interpretación de los resultados.\n\n")

        # Mostrar tabla de resultados (si aplica)
        if self.tipo_visualizacion.get() in ["Tabla 📊", "Ambos 🧩"]:
            if 'frecuencias' in resultados:
                tabla = resultados['frecuencias'].to_frame().to_string()
                self.area_resultados.insert("end", f"📈 Frecuencias:\n{tabla}\n\n")
            else:
                # Mostrar estadísticas
                stats = {k: v for k, v in resultados.items() if k not in ['interpretacion', 'probabilidades']}
                tabla = pd.DataFrame(list(stats.items()), columns=['📌 Métrica', '🔢 Valor']).to_string(index=False)
                self.area_resultados.insert("end", f"📊 Estadísticas:\n{tabla}\n\n")

        # Mostrar gráficos
        if self.tipo_visualizacion.get() in ["Gráfico 📈", "Ambos 🧩"]:
            self.mostrar_graficos(resultados)

    def mostrar_graficos(self, resultados):
        """
        Muestra los gráficos generados en la interfaz.

        :param resultados: Diccionario con rutas de los gráficos generados.
        """
        # Limpiar gráficos anteriores
        for widget in self.panel_resultados.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and hasattr(widget, 'image'):
                widget.destroy()

        # Mostrar nuevos gráficos
        for key in ['grafico_distribucion', 'grafico_caja', 'grafico_barras']:
            ruta = resultados.get(key)
            if ruta and os.path.exists(ruta):
                try:
                    img = Image.open(ruta)
                    # Obtener tamaño dinámico basado en el panel_resultados
                    panel_width = self.panel_resultados.winfo_width()
                    if panel_width < 200:
                        panel_width = 800
                    img_width = min(400, panel_width - 100)
                    img_height = int(img_width * img.height / img.width)
                    img = img.resize((img_width, img_height), Image.LANCZOS)
                    img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(img_width, img_height))
                    label_imagen = ctk.CTkLabel(self.panel_resultados, image=img_ctk, text="", corner_radius=10)
                    label_imagen.image = img_ctk  # Mantener referencia
                    label_imagen.pack(pady=10)
                except Exception as e:
                    logging.exception(f"Error al mostrar el gráfico '{ruta}': {e}")

    def mostrar_datos(self):
        """
        Muestra los datos de la muestra en una nueva ventana.
        """
        if self.sample is not None:
            try:
                top = ctk.CTkToplevel(self.app)
                top.title("📋 Datos de la Muestra")
                top.geometry("800x600")
                top.configure(bg="#F9F9F9")

                tree = ttk.Treeview(top, columns=list(self.sample.columns), show="headings")
                tree.pack(fill="both", expand=True)

                # Estilizar las columnas
                style = ttk.Style()
                style.theme_use("clam")
                style.configure("Treeview",
                                background="#FFFFFF",
                                foreground="#333333",
                                rowheight=25,
                                fieldbackground="#FFFFFF")
                style.map('Treeview', background=[('selected', '#347083')])

                for col in self.sample.columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center")

                for _, row in self.sample.iterrows():
                    tree.insert("", "end", values=list(row))

                logging.info("Datos de la muestra mostrados en una nueva ventana.")
            except Exception as e:
                logging.exception(f"Error al mostrar datos de la muestra: {e}")
                messagebox.showerror("❌ Error", f"Ocurrió un error al mostrar los datos: {e}")
        else:
            messagebox.showerror("❌ Error", "No hay datos para mostrar.")
            logging.warning("Intento de mostrar datos sin crear muestra.")

    def generar_pdf(self):
        """
        Genera el informe PDF del último análisis realizado.
        """
        if self.resultados and self.columna_actual:
            try:
                self.analisis.generar_informe_pdf(self.columna_actual, self.resultados)
                messagebox.showinfo("📄 Informe PDF", "El informe PDF ha sido generado y guardado en la carpeta 'PDF'.")
                logging.info(f"Informe PDF para '{self.columna_actual}' generado correctamente.")
            except Exception as e:
                logging.exception(f"Error al generar el informe PDF: {e}")
                messagebox.showerror("❌ Error", f"Ocurrió un error al generar el informe PDF: {e}")
        else:
            messagebox.showerror("❌ Error", "No hay resultados disponibles para generar un PDF.")
            logging.warning("Intento de generar PDF sin resultados disponibles.")

    def ejecutar(self):
        """
        Ejecuta el bucle principal de la interfaz gráfica.
        """
        self.app.mainloop()