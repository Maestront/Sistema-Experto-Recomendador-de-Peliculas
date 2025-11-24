import pandas as pd
import json
import os

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
#   FUNCIONES: guardar y cargar opciones precalculadas
# =====================================================
def guardar_opciones(df, path="opciones.json"):
    opciones = {
        "generos": obtener_generos_disponibles(df),
        "ratings": sorted(df["averageRating"].dropna().unique().tolist()),
        "años": sorted(df["startYear"].dropna().unique().tolist())
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(opciones, f, ensure_ascii=False, indent=4)

def cargar_opciones(path="opciones.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# =====================================================
#   CARGA DE DATASETS
# =====================================================
def cargar_datasets():
    basics = pd.read_csv("title.basics.tsv.gz", sep="\t", low_memory=False)
    ratings = pd.read_csv("title.ratings.tsv.gz", sep="\t", low_memory=False)
    names = pd.read_csv("name.basics.tsv.gz", sep="\t", low_memory=False)[["nconst","primaryName"]]

    # Limpieza básica
    basics = basics[basics["titleType"].isin(["movie", "tvSeries", "short", "tvMovie"])]
    basics = basics[basics["startYear"] != "\\N"]
    basics["startYear"] = basics["startYear"].astype(int)
    basics["runtimeMinutes"] = basics["runtimeMinutes"].replace("\\N", pd.NA)
    basics["genres"] = basics["genres"].replace("\\N", "")

    df = basics.merge(ratings, on="tconst", how="left")
    df["averageRating"] = df["averageRating"].fillna(0)

    # Principals
    principals = pd.read_csv("title.principals.tsv.gz", sep="\t", low_memory=False)
    principals = principals[principals["category"].isin(["actor", "actress", "director"])]
    principals = principals.merge(names, on="nconst", how="left")

    # Merge final
    df_full = df.merge(principals, on="tconst", how="left")

    return df, df_full

# =====================================================
#   FUNCIONES DE RECOMENDACIÓN
# =====================================================
def recomendar_simple(df, genero=None, rating_minimo=7.0, limite=20):
    df_copy = df.copy()
    if genero:
        if isinstance(genero, str):
            genero = [genero]
        for g in genero:
            df_copy = df_copy[df_copy["genres"].str.contains(g, case=False, na=False)]
    df_copy = df_copy[df_copy["averageRating"] >= rating_minimo]
    df_copy = df_copy.sort_values(by="averageRating", ascending=False)
    return df_copy.head(limite)

def recomendar(df_full, generos=None, tipo="movie", rating_minimo=0.0, inicio=1900, fin=2025,
               min_duracion=None, max_duracion=None, persona=None, limite=20):
    df = df_full.copy()

    if tipo:
        df = df[df["titleType"] == tipo]
    df = df[(df["startYear"] >= inicio) & (df["startYear"] <= fin)]
    df = df[df["averageRating"] >= rating_minimo]

    if generos:
        if isinstance(generos, str):
            generos = [generos]
        for g in generos:
            df = df[df["genres"].str.contains(g, case=False, na=False)]

    if min_duracion is not None:
        df = df[df["runtimeMinutes"] >= min_duracion]
    if max_duracion is not None:
        df = df[df["runtimeMinutes"] <= max_duracion]

    if persona:
        df = df[df["primaryName"].str.contains(persona, case=False, na=False)]

    df = df.sort_values(by="averageRating", ascending=False)
    df = df.drop_duplicates(subset="tconst")
    return df.head(limite)

# =====================================================
#   INICIO: carga y precarga de opciones
# =====================================================
df_imdb, df_imdb_full = cargar_datasets()

opciones = cargar_opciones()
if not opciones:
    guardar_opciones(df_imdb)
    opciones = cargar_opciones()

print("\n===== OPCIONES DISPONIBLES =====")
print("\nGéneros disponibles:")
for g in opciones["generos"]:
    print(f" - {g}")

print("\nRatings disponibles:")
print(" - " + ", ".join(map(str, opciones["ratings"])))

print("\nAños disponibles:")
print(" - " + ", ".join(map(str, opciones["años"])))
print("\n=================================\n")
