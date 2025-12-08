import os
import pandas as pd
import pickle
import requests
import numpy as np

# Obtener ruta absoluta del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "final_dataset.pkl")

# --- Variables de configuración de TMDB ---
TMDB_API_KEY = "72fcadc100cf32eae46ac40b28d0e186" # Clave de API
TMDB_BASE_URL = "https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w185" # URL base para imágenes
# ------------------------------------------


# ============================================================
# CARGA DEL DATASET
# ============================================================
def cargar_dataset():
    """Carga el dataset de películas, asegura tipos y formatea datos."""
    try:
        with open(DATASET_PATH, "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {DATASET_PATH}")
        return pd.DataFrame()

    movies = data.get("movies", [])
    df = pd.DataFrame(movies)

    if df.empty:
        return df

    # Asegurar tipos
    df["rating"] = df.get("rating", pd.NA).astype(float)
    df["votes"] = df.get("votes", pd.NA).astype(int)
    df["tconst"] = df.get("tconst", pd.NA) 
    df["year"] = pd.to_numeric(df.get("year", pd.NA), errors="coerce")

    # CORRECCIÓN DE GÉNEROS: Asegurar que es una lista de strings
    def safe_to_list(g):
        if isinstance(g, list):
            return [str(x) for x in g]
        if isinstance(g, str):
            try:
                # Intenta evaluar la cadena si tiene formato de lista (ej: "['Drama', 'Action']")
                return [str(x) for x in eval(g)]
            except:
                # Si es una cadena simple (ej: "Drama,Action") o falla, la devuelve
                return [g.strip() for g in g.split(',') if g.strip()]
        return []

    df["genres"] = df.get("genres", [[]] * len(df)).apply(safe_to_list)

    return df

# ============================================================
# EXTRACCIÓN DE GÉNEROS (Para llenar el multiselect en app.py)
# ============================================================
def obtener_lista_generos():
    """Carga el dataset y extrae todos los géneros únicos disponibles del índice."""
    
    try:
        with open(DATASET_PATH, "rb") as f:
            data = pickle.load(f)
    except FileNotFoundError:
        return []

    genres_data = data.get("genres", {}) 
    
    # ----------------------------------------------------
    # --- CORRECCIÓN: Filtra géneros no válidos ---
    # ----------------------------------------------------
    generos_unicos = [
        g for g in genres_data.keys() 
        if g.strip() and g != r'\N' and g != r'N'
    ]
    # ----------------------------------------------------
    
    # Ordenar alfabéticamente
    generos_unicos = sorted(generos_unicos)
    
    return generos_unicos

# ============================================================
# FILTRO POR PERFIL (Popularidad)
# ============================================================
def filtrar_por_perfil(df, perfil):
    """Filtra el DataFrame según el umbral de votos del perfil de popularidad."""

    if perfil == "mainstream":
        return df[df["votes"] >= 30000]
    elif perfil == "mixed":
        return df[(df["votes"] >= 5000) & (df["votes"] < 30000)]
    elif perfil == "niche":
        return df[df["votes"] < 5000]

    return df


# ============================================================
# WEIGHTED RATING (WR)
# ============================================================
def weighted_rating(row, C=0, M=3000):
    """Calcula el Weighted Rating (WR) de una película."""
    R = row["rating"]
    v = row["votes"]
    
    return (v / (v + M)) * R + (M / (v + M)) * C


# ============================================================
# OBTENER URLS DE PÓSTERES DESDE TMDB (Consulta Dinámica)
# ============================================================
def obtener_urls_posters(df_resultados):
    """
    Consulta la API de TMDB para obtener las URLs de los pósteres
    basándose en el ID de IMDb (tconst).
    """
    poster_urls = {}
    
    # Solo procesamos IDs que son cadenas y no son nulos
    imdb_ids = df_resultados['tconst'].dropna().astype(str).unique()
    
    for imdb_id in imdb_ids:
        # Consulta la API de TMDB usando el ID de IMDb (tconst)
        url = TMDB_BASE_URL.format(imdb_id=imdb_id, api_key=TMDB_API_KEY)
        
        try:
            response = requests.get(url, timeout=3)
            data = response.json()
            
            # --- LÓGICA DE EXTRACCIÓN ROBUSTA ---
            poster_path = None
            
            # 1. Verificar si hay resultados de películas y obtener el primer resultado
            if data.get('movie_results'):
                movie_result = data['movie_results'][0]
                
                # 2. Obtener el poster_path si existe y no es nulo
                if movie_result.get('poster_path'):
                    poster_path = movie_result['poster_path']
            
            # 3. Mapear la URL
            if poster_path:
                poster_urls[imdb_id] = IMAGE_BASE_URL + poster_path
            else:
                poster_urls[imdb_id] = None # No se encontró póster
            # --- FIN LÓGICA DE EXTRACCIÓN ROBUSTA ---
                
        except requests.exceptions.RequestException:
            # Asignación de None si falla la conexión HTTP
            poster_urls[imdb_id] = None
        except Exception:
            # Manejo de cualquier otra excepción (ej. error de JSON)
            poster_urls[imdb_id] = None
            
    # Mapear las URLs de vuelta al DataFrame
    df_resultados['poster_url'] = df_resultados['tconst'].map(poster_urls)
    
    # Convertir NaN a None para evitar errores en la interfaz
    df_resultados['poster_url'] = df_resultados['poster_url'].replace({np.nan: None})
    
    return df_resultados


# ============================================================
# RECOMENDADOR PRINCIPAL
# ============================================================
def obtener_recomendaciones_df(generos_seleccionados, perfil, df_completo, n=20, orden='Weighted Rating (Default)'):
    """
    Filtra y recomienda películas basadas en el perfil, géneros (AND) y un criterio de ordenamiento.
    """
    
    filtrado = df_completo.copy()

    # 1. Filtro por Género (Lógica "AND")
    if generos_seleccionados:
        
        def check_all_genres(movie_genres_list, required_genres):
            return all(g in movie_genres_list for g in required_genres)

        filtrado = filtrado[
            filtrado['genres'].apply(
                lambda x: check_all_genres(x, generos_seleccionados)
            )
        ]

    if filtrado.empty:
        return pd.DataFrame()

    # 2. Filtrar por ID de IMDb válido (CRÍTICO para pósteres)
    filtrado = filtrado[filtrado['tconst'].notna()]
    
    # 3. Filtrar por perfil (Popularidad)
    filtrado = filtrar_por_perfil(filtrado, perfil)

    if filtrado.empty:
        return pd.DataFrame()

    # 4. Calcular Weighted Rating (WR)
    C = filtrado["rating"].mean()
    M = 3000
    
    filtrado["wr"] = filtrado.apply(lambda r: weighted_rating(r, C=C, M=M), axis=1)

    # 5. Ordenar y Limitar
    if orden == 'Año de Estreno (Reciente)':
        sort_column = 'year'
        ascending = False
    elif orden == 'Número de Votos':
        sort_column = 'votes'
        ascending = False
    else: # 'Weighted Rating (Default)'
        sort_column = 'wr'
        ascending = False

    top = filtrado.sort_values(sort_column, ascending=ascending).head(n)

    # 6. Obtener URLs de Pósteres y Formatear Salida
    top_with_posters = obtener_urls_posters(top.copy()) 
    
    resultados_ui = top_with_posters[[
        "title",
        "year",
        "genres",
        "wr",
        "rating",
        "votes",
        "poster_url" 
    ]].rename(columns={
        "title": "primaryTitle",
        "rating": "averageRating" 
    })

    return resultados_ui


if __name__ == "__main__":
    df = cargar_dataset()
    if not df.empty:
        print("=== TEST: Drama Y Action (mixed) ===")
        resultados_test = obtener_recomendaciones_df(["Drama", "Action"], perfil="mixed", df_completo=df, n=5)
        print(resultados_test[['primaryTitle', 'wr', 'genres', 'poster_url']].to_string())
    else:
        print("No se pudo cargar el dataset para el test. Verifica la ruta o el archivo.")