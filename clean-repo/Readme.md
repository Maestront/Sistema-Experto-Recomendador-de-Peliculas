# 🎬 Sistema Experto Recomendador de Películas  
### Basado en IMDb – Python + Pandas + Sistema Híbrido de Recomendación

Este proyecto implementa un **sistema experto recomendador de películas** usando los datasets oficiales de **IMDb** (TSV.GZ).  
Genera un dataset optimizado y aplica un algoritmo híbrido que combina:

- Filtrado por género  
- Segmentación por popularidad (mainstream, mixed, niche)  
- Weighted Rating (IMDB)  
- Selección diversa dentro de cada segmento  

---

## 📁 Estructura del repositorio

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

yaml


---

## 📥 1. Descargar los datos de IMDb

El sistema usa **4 archivos oficiales de IMDb** (gratuitos):

| Archivo | Descripción |
|--------|-------------|
| `title.basics.tsv.gz` | Información general de películas |
| `title.ratings.tsv.gz` | Ratings y votos |
| `title.principals.tsv.gz` | Actores, directores, escritores |
| `name.basics.tsv.gz` | Información de personas |

Descárgalos desde:  
📌 https://datasets.imdbws.com/

Luego colócalos en:

data/raw/

yaml


---

## ⚙️ 2. Preparar los datos (primer script)

Ejecuta:

python src/prepare_data.py

Esto generará:

data/processed/optimized_data.pkl

Contiene:

Diccionario tconst → info completa

Índice por géneros

Diccionario de personas

Índice invertido de nombres

🧩 3. Crear el dataset final
Ejecuta:

python src/final_dataset.py


Genera:

data/processed/final_dataset.pkl
Listo para búsquedas y recomendaciones.

🤖 4. Usar el recomendador

Ejemplo desde consola:

python src/recomendador.py
Ejemplo desde Python:

python

from recomendador import recomendar_por_genero

recs = recomendar_por_genero("Action", perfil="mixed", n=20)

for r in recs:
    print(r["title"], r["rating"], r["votes"])
🧠 ¿Cómo funciona el recomendador?
✔ Segmentación por popularidad
Se usan percentiles automáticos:

Mainstream → top 20% en votos

Mixed → rango medio

Niche → películas con pocos votos

✔ Perfiles de recomendación
mainstream → películas populares

mixed → equilibrio entre populares y raras

niche → películas poco conocidas

auto → 50% / 20% / 30%

🧪 Ejemplo de salida
java

=== RECOMENDACIONES (Action - mixed) ===
Mad Max: Fury Road (2015) | WR 8.75 | Rating 8.1 | Votes 1,000,000
John Wick (2014) | WR 8.32 | Rating 7.4 | Votes 600,000
...

🚀 Requisitos
Python 3.10+

pandas

numpy

Instalar:


pip install -r requirements.txt
🏷 Versionado (SemVer)
Usa SemVer. Ejemplo:


git tag -a v1.1.0 -m "Versión estable"
git push --tags