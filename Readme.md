# 🎬 Sistema Experto Recomendador de Películas

**Autor:** [Edmundo Emiliano Sánchez Zúñiga]
**Versión:** 2.1.0 (Estable)

Este proyecto implementa un Sistema Experto Recomendador de Películas basado en datos de IMDb, utilizando un algoritmo de *Weighted Rating* para ofrecer recomendaciones objetivas y personalizadas a los usuarios mediante una interfaz interactiva de Streamlit.

---

## ✨ Características Clave del Sistema

* **Algoritmo de Weighted Rating (WR):** Utiliza la fórmula WR para clasificar las películas de manera objetiva, balanceando la calificación promedio y el número de votos, priorizando títulos con alta popularidad y buena crítica.
* **Recomendaciones Filtradas:** Permite al usuario filtrar las películas basándose en:
    * **Géneros:** Búsqueda avanzada por uno o múltiples géneros.
    * **Popularidad:** Opciones de perfil *Mainstream* (ampliamente votadas) o *Niche* (menos conocidas pero bien valoradas).
* **Integración de Metadatos:** Conectividad con la API de The Movie Database (TMDB) para obtener las **URLs de los pósteres** de las películas y mejorar la experiencia visual en la interfaz.
* **Interfaz de Usuario (Streamlit):** Una aplicación web simple e intuitiva para interactuar con el motor de recomendaciones.

---

## 🛠️ Configuración e Instalación

### 1. Clonar el Repositorio

Clona este repositorio a tu máquina local:

```bash
git clone [https://github.com/Maestront/Sistema-Experto-Recomendador-de-Peliculas.git](https://github.com/Maestront/Sistema-Experto-Recomendador-de-Peliculas.git)
cd Sistema-Experto-Recomendador-de-Peliculas

```
2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv
# Activar entorno en Windows
.\venv\Scripts\activate
# Activar entorno en macOS/Linux
source venv/bin/activate
```
3. Instalar Dependencias
Instala todas las librerías necesarias (como Streamlit, pandas, requests, etc.):

```bash
pip install -r requirements.txt
```
💾 Preparación de Datos (Paso Crucial)
Debido al gran tamaño de los archivos de dataset procesados (superiores al límite de 2 GB de GitHub LFS), estos se alojan en Hugging Face Hub. Es obligatorio descargar estos archivos antes de ejecutar la aplicación.

Ejecuta el script de descarga:

```bash

python src/download_data.py
```
Este comando:

Creará la carpeta data/processed/.

Descargará automáticamente los archivos final_dataset.pkl y optimized_data.pkl y los colocará en la carpeta data/processed/.

🚀 Ejecución de la Aplicación
Una vez que la descarga de datos haya finalizado, puedes iniciar la aplicación Streamlit:

```bash

python -m streamlit run app.py
```
Tu navegador abrirá automáticamente la interfaz del Sistema Experto Recomendador de Películas.