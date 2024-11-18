# Archivo: main.py

import customtkinter as ctk
from modules.interfaz import InterfazUsuario
import logging
import sys

def manejar_excepciones(tipo, valor, traceback):
    logging.exception("Excepción no manejada: ", exc_info=(tipo, valor, traceback))

def main():
    # Configurar el registro de errores
    logging.basicConfig(
        filename='errores.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.ERROR
    )
    sys.excepthook = manejar_excepciones

    app = ctk.CTk()
    app.title("Análisis Estadístico de Biblioteca")
    app.geometry("1280x800")
    app.minsize(1024, 768)

    interfaz = InterfazUsuario(app)
    interfaz.ejecutar()

if __name__ == "__main__":
    main()