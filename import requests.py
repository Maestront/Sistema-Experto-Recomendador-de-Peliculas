import pandas as pd

# Cargar archivo IMDb
movies = pd.read_csv("title.basics.tsv.gz", sep="\t", low_memory=False)

# Convertir valores "\N" en NaN
movies = movies.replace({"\\N": None})

# Filtrar por tipo de título (ej: movie, short, tvMovie)
movies = movies[movies["titleType"] == "movie"]


def filtrar_peliculas(
    genero=None,
    generos_varios=None,
    anio_min=None,
    anio_max=None,
    duracion_min=None,
    duracion_max=None,
    palabras_titulo=None
):
    """
    Retorna una lista filtrada de películas.
    Todos los filtros son opcionales.
    """

    df = movies.copy()

    # ---- Filtro por género único ----
    if genero:
        df = df[df["genres"].str.contains(genero, na=False)]

    # ---- Filtro por lista de géneros ----
    if generos_varios:
        filtro_generos = df["genres"].str.split(",").apply(
            lambda g: any(gg in g for gg in generos_varios) if g else False
        )
        df = df[filtro_generos]

    # ---- Filtro por rango de años ----
    if anio_min:
        df = df[df["startYear"].astype(float) >= float(anio_min)]
    if anio_max:
        df = df[df["startYear"].astype(float) <= float(anio_max)]

    # ---- Filtro por duración ----
    if duracion_min:
        df = df[df["runtimeMinutes"].astype(float) >= float(duracion_min)]
    if duracion_max:
        df = df[df["runtimeMinutes"].astype(float) <= float(duracion_max)]

    # ---- Filtro por palabras clave en título ----
    if palabras_titulo:
        df = df[df["primaryTitle"].str.contains(palabras_titulo, case=False, na=False)]

    return df


# ---------------------------------------------
# EJEMPLOS DE USO
# ---------------------------------------------

# 1. Películas solo de acción
ejemplo1 = filtrar_peliculas(genero="Action")

# 2. Películas que mezclen varios géneros
ejemplo2 = filtrar_peliculas(generos_varios=["Action", "Sci-Fi"])

# 3. Películas del 2000 al 2010
ejemplo3 = filtrar_peliculas(anio_min=2000, anio_max=2010)

# 4. Películas de terror más cortas de 100 minutos
ejemplo4 = filtrar_peliculas(genero="Horror", duracion_max=100)

# 5. Películas cuyo título contenga “dragon”
ejemplo5 = filtrar_peliculas(palabras_titulo="dragon")

print(ejemplo5.head())
