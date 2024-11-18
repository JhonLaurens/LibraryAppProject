# Análisis Estadístico de Datos de Biblioteca

Esta aplicación proporciona una interfaz gráfica para cargar, analizar y visualizar datos de una biblioteca utilizando Python y CustomTkinter. Permite realizar análisis estadísticos descriptivos de variables cualitativas y cuantitativas, incluyendo la creación de muestras aleatorias simples y estratificadas.  
Desarrollada por [github.com/JhonLaurens](https://github.com/JhonLaurens).

---

## Funcionalidades

- **Carga de datos**  
  Permite cargar datos desde un archivo Excel (`.xlsx` o `.xls`) que debe contener al menos las siguientes columnas:  
  `ITEM`, `DOCUMENTO`, `NOMBRE`, `EDAD`, `GENERO`, `ESTRATO`, `TIPO LIBROS`, `TIPO USUARIO`, `SEDE`, `TIEMPO DE PRESTAMO`.

- **Creación de muestras**  
  Ofrece dos métodos de muestreo:
  - **Muestreo Aleatorio Simple**: Selecciona una muestra aleatoria del conjunto de datos.
  - **Muestreo Estratificado Proporcional**: Crea una muestra estratificada por el campo `ESTRATO`, manteniendo las proporciones de cada estrato en la muestra. *(Requiere que la columna `ESTRATO` exista en el archivo)*.
  - **Tamaño de muestra personalizado**: Permite especificar el tamaño de la muestra deseada.

- **Análisis Estadístico**  
  Realiza análisis descriptivos de variables:
  - **Variables categóricas (cualitativas)**:  
    - Calcula frecuencias y moda.  
    - Genera diagramas de barras y gráficos circulares.
  - **Variables numéricas (cuantitativas)**:  
    - Calcula medidas como media, mediana, moda, desviación estándar, varianza, coeficiente de variación, cuartiles, rango intercuartílico, valores atípicos.  
    - Realiza pruebas de normalidad (Shapiro-Wilk).  
    - Genera gráficos como histogramas con curva de densidad, diagramas de caja (*boxplot*) y gráficos Q-Q.

- **Visualización**  
  Presenta resultados con gráficos de alta calidad usando Matplotlib y Seaborn.

- **Interpretación de Resultados**  
  Proporciona una guía para facilitar la comprensión de los análisis.

- **Gestión de Errores**  
  Incluye una robusta gestión de errores para informar sobre problemas durante la carga de archivos, creación de muestras o análisis.

- **Interfaz Gráfica**  
  Diseñada con CustomTkinter para una experiencia moderna y fácil de usar.

- **Temas Personalizables**  
  Permite cambiar entre temas de color (Azul, Verde, Oscuro).

---

## Requisitos

- **Python 3.7+**  
  La aplicación está desarrollada en Python.

- **Librerías de Python necesarias**  
  Instálalas con el siguiente comando:

  ```bash
  pip install customtkinter pandas numpy matplotlib seaborn scipy openpyxl

  ## Instrucciones de Uso

1. **Clonar el repositorio**  
   Clona el repositorio desde GitHub a tu computadora local.

2. **Instalar dependencias**  
   Instala las librerías necesarias (ver sección ["Requisitos"](#requisitos)).

3. **Ejecutar la aplicación**  
   Ejecuta el archivo principal de la aplicación (ejemplo: `main.py`).

4. **Cargar archivo**  
   Haz clic en el botón **"Cargar Archivo Excel"** y selecciona un archivo Excel que contenga los datos de la biblioteca.  
   *(Asegúrate de que el archivo tenga las columnas requeridas; ver sección ["Columnas Requeridas"](#columnas-requeridas)).

5. **Crear muestra**  
   Selecciona el método de muestreo (aleatorio simple o estratificado) y especifica el tamaño deseado.

6. **Realizar análisis**  
   Selecciona las variables a analizar (`Género`, `Estrato`, `Edad`, `Tiempo de préstamo`) y revisa los resultados en el panel **"Resultados del Análisis"**.

7. **Interpretar resultados**  
   Usa la guía de interpretación para comprender el significado de los resultados.

---

## Columnas Requeridas

El archivo Excel debe contener las siguientes columnas:  

- **`ITEM`**: Número de ítem o identificador único.  
- **`DOCUMENTO`**: Número de documento del usuario.  
- **`NOMBRE`**: Nombre del usuario.  
- **`EDAD`**: Edad del usuario.  
- **`GENERO`**: Género del usuario (ejemplo: Masculino, Femenino, Otro).  
- **`ESTRATO`**: Estrato socioeconómico del usuario.  
- **`TIPO LIBROS`**: Tipo de libros prestados (ejemplo: Novela, Científico, Infantil).  
- **`TIPO USUARIO`**: Tipo de usuario (ejemplo: Estudiante, Docente, Público).  
- **`SEDE`**: Sede de la biblioteca donde se realizó el préstamo.  
- **`TIEMPO DE PRESTAMO`**: Duración del préstamo (ejemplo: días, semanas, meses).

---

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras errores o quieres sugerir mejoras:  

- Abre un **issue** en el repositorio de GitHub.  
- Realiza un **pull request** con las mejoras propuestas.


