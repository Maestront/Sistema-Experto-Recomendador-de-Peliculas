# 🎬 Sistema Experto Recomendador de Películas

## Descripción del Proyecto

Este proyecto implementa un Sistema Experto para la recomendación de películas basado en datos de IMDb y The Movie Database (TMDB). El sistema utiliza el algoritmo de **Weighted Rating (WR)** para clasificar títulos y permite al usuario filtrar las recomendaciones según **géneros**, **perfil de popularidad** (*Mainstream*, *Mixed*, *Niche*), y **criterio de ordenamiento**.

La interfaz de usuario está desarrollada con **Streamlit**, ofreciendo una experiencia interactiva y visualmente atractiva con la carga dinámica de portadas de películas obtenidas a través de la API de TMDB, y un diseño optimizado con CSS Flexbox para el centrado de los elementos.

## Estructura del Repositorio

clean-repo/
│
├── src/
│ ├── prepare_data.py # Procesa los 4 TSV de IMDB → optimized_data.pkl
│ ├── final_dataset.py # Convierte optimized → final_dataset.pkl
│ └── recomendador.py # Algoritmo de recomendación
│
├── data/
│ ├── raw/ # Archivos originales IMDb (.tsv.gz)
│ └── processed/ # Pickles generados (optimized y final)
│
└── README.md

## 🚀 Requisitos e Instalación

### Requisitos Previos

* **Python 3.8+**
* Una clave de API de **The Movie Database (TMDB)**.

### Pasos de Instalación

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/Maestront/Sistema-Experto-Recomendador-de-Peliculas.git](https://github.com/Maestront/Sistema-Experto-Recomendador-de-Peliculas.git)
    cd Sistema-Experto-Recomendador-de-Peliculas
    ```

2.  **Crear y Activar el Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # En Linux/macOS
    venv\Scripts\activate      # En Windows
    ```

3.  **Instalar Dependencias:**
    Instala todas las librerías necesarias con el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## 💾 Preparación de Datos

El sistema necesita datos de IMDb. **Asegúrate de ejecutar estos pasos después de instalar las dependencias:**

1.  **Descargar Datos de IMDb:**
    Descarga los siguientes archivos TSV.GZ desde la página oficial de [IMDb datasets](https://datasets.imdbws.com/):
    * `title.basics.tsv.gz`
    * `title.ratings.tsv.gz`
    * `title.principals.tsv.gz`
    * `name.basics.tsv.gz`

2.  **Mover Archivos:** Coloca los cuatro archivos `.tsv.gz` descargados en la carpeta `data/raw/`.

3.  **Procesar los Datos:** Ejecuta los scripts de preparación y construcción del *dataset* final para generar `final_dataset.pkl`.
    ```bash
    python src/prepare_data.py
    python src/build_final_dataset.py
    ```

## 💻 Ejecución de la Aplicación

Una vez que tengas el `final_dataset.pkl`, inicia la interfaz de Streamlit:

```bash
python -m streamlit run app.py

La aplicación se abrirá en tu navegador.

⚙️ Tecnologías Utilizadas
Lenguaje: Python

Librerías: Pandas, NumPy, Requests.

Interfaz de Usuario: Streamlit

Fuente de Datos: IMDb y TMDB API