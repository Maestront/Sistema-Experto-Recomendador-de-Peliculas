import pandas as pd

# =====================================================
#   FUNCIÓN: obtener lista de géneros disponibles
# =====================================================

def obtener_generos_disponibles(df):
    generos = set()
    for lista in df["genres"].dropna():
        for g in lista.split(","):
            if g.strip() != "":
                generos.add(g.strip())
    return sorted(generos)


# =====================================================
#   FUNCIÓN: mostrar opciones de filtrado
# =====================================================

def mostrar_opciones(df):
    print("\n===== OPCIONES DISPONIBLES =====")

    # --- Géneros ---
    generos = obtener_generos_disponibles(df)
    print("\nGéneros disponibles:")
    for g in generos:
        print(f" - {g}")

    # --- Ratings ---
    print("\nRatings disponibles:")
    ratings = sorted(df["averageRating"].dropna().unique())
    print(" - " + ", ".join(map(str, ratings)))

    # --- Años ---
    print("\nAños disponibles:")
    años = sorted(df["startYear"].dropna().unique())
    print(" - " + ", ".join(map(str, años)))

    print("\n=================================\n")


# =====================================================
#   CARGA DE DATASETS
# =====================================================

def cargar_datasets():
    basics = pd.read_csv("title.basics.tsv.gz", sep="\t", low_memory=False)
    ratings = pd.read_csv("title.ratings.tsv.gz", sep="\t", low_memory=False)

    # Limpieza básica
    basics = basics[basics["titleType"].isin(["movie", "tvSeries", "short", "tvMovie"])]
    basics = basics[basics["startYear"] != "\\N"]

    basics["startYear"] = basics["startYear"].astype(int)
    basics["runtimeMinutes"] = basics["runtimeMinutes"].replace("\\N", pd.NA)
    basics["genres"] = basics["genres"].replace("\\N", "")

    df = basics.merge(ratings, on="tconst", how="left")
    df["averageRating"] = df["averageRating"].fillna(0)

    return df


# Cargar solo una vez
df_imdb = cargar_datasets()


# =====================================================
#   FUNCIÓN PRINCIPAL DE RECOMENDACIÓN (completa)
# =====================================================

def recomendar(
    generos=None,
    inicio=1900,
    fin=2025,
    rating_minimo=0.0,
    tipo="movie",
    limite=20
):
    df = df_imdb.copy()

    # Filtro por tipo
    if tipo:
        df = df[df["titleType"] == tipo]

    # Año
    df = df[(df["startYear"] >= inicio) & (df["startYear"] <= fin)]

    # Rating
    df = df[df["averageRating"] >= rating_minimo]

    # Géneros
    if generos:
        for g in generos:
            df = df[df["genres"].str.contains(g, case=False, na=False)]

    # Orden final
    df = df.sort_values(by="averageRating", ascending=False)

    return df.head(limite)


# =====================================================
#   NUEVA FUNCIÓN v1.1: RECOMENDACIÓN SENCILLA
# =====================================================

def recomendar_simple(
    genero=None,
    rating_minimo=7.0,
    limite=20
):
    """
    Recomendación simple.
    Parámetros mínimos para el usuario:
        - genero (string)
        - rating_minimo (float)
        - limite (int)
    """
    df = df_imdb.copy()

    if genero:
        df = df[df["genres"].str.contains(genero, case=False, na=False)]

    df = df[df["averageRating"] >= rating_minimo]

    df = df.sort_values(by="averageRating", ascending=False)

    return df.head(limite)


# =====================================================
#   Mostrar opciones al inicio
# =====================================================

mostrar_opciones(df_imdb)

# Ejemplo de llamada simple:
# print(recomendar_simple(genero="Action", rating_minimo=8))
