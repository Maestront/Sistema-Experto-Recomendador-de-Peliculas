📽️ Sistema Experto Recomendador de Películas

Proyecto de Sistemas Expertos – CETI

Este proyecto implementa un sistema experto capaz de recomendar películas basado en características como género, duración, calificación, popularidad, año, entre otras.
El objetivo es ofrecer sugerencias mediante reglas lógicas y procesamiento de datos.

🚀 Características principales

Limpieza y preparación del dataset original.

Generación de un dataset final optimizado.

Motor de recomendación basado en reglas (no machine learning).

Scripts modulares y fáciles de entender.

Compatible con Python 3.10+.

📂 Estructura del proyecto
.
├── recomendador.py        # Motor de reglas para recomendaciones
├── prepare_data.py        # Limpieza y preprocesamiento del dataset
├── final_dataset.py       # Generación del dataset final (si aplica)
├── requirements.txt       # Dependencias del proyecto
├── README.md
├── .gitignore
└── data/
    ├── raw/               # Datos originales (git ignore)
    └── processed/         # Datos limpios (git ignore)

🛠️ Instalación
1. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

2. Instalar dependencias

Si tienes un archivo requirements.txt:

pip install -r requirements.txt

📊 Uso del sistema
1. Preparar datos
python prepare_data.py

2. Generar dataset final (si aplica)
python final_dataset.py

3. Ejecutar el recomendador
python recomendador.py

🧠 Lógica del sistema experto

A diferencia de otros recomendadores, este proyecto utiliza reglas explícitas en lugar de modelos matemáticos.

Ejemplo de regla:

Si el usuario prefiere acción AND la película tiene rating mayor a 8 → recomendar


Puedes editar las reglas directamente dentro de recomendador.py para personalizar el comportamiento.

📌 Requisitos

Python 3.10 o superior

Pandas

Numpy

(opcional) Jupyter Notebook si deseas explorar los datos

🏷️ Versionado

Se utiliza Semantic Versioning (SemVer):

MAJOR.MINOR.PATCH


Versión actual estable: v0.2.1-clean

🧑‍💻 Autor

Edmundo Sánchez
Proyecto escolar – CETI