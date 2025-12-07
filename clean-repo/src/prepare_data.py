import pandas as pd
import pickle
import os

# ==========================
#  RUTAS ABSOLUTAS
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

BASICS_PATH = os.path.join(RAW_DIR, "title.basics.tsv.gz")
RATINGS_PATH = os.path.join(RAW_DIR, "title.ratings.tsv.gz")
PRINCIPALS_PATH = os.path.join(RAW_DIR, "title.principals.tsv.gz")
NAME_BASICS_PATH = os.path.join(RAW_DIR, "name.basics.tsv.gz")

OUTPUT_PICKLE = os.path.join(PROCESSED_DIR, "optimized_data.pkl")


# ==========================
#  CARGA SEGURA DE TSV.GZ
# ==========================
def load_tsv_gz(path):
    print(f"Cargando archivo: {path}")
    return pd.read_csv(path, sep="\t", low_memory=False, compression='gzip')


# ==========================
#  PROCESAMIENTO
# ==========================
def crear_diccionarios():
    print("\n=== Cargando datasets IMDB… ===")

    basics = load_tsv_gz(BASICS_PATH)
    ratings = load_tsv_gz(RATINGS_PATH)
    principals = load_tsv_gz(PRINCIPALS_PATH)
    names = load_tsv_gz(NAME_BASICS_PATH)

    # ================================================
    # LIMPIEZA
    # ================================================
    print("Limpieza básica...")

    basics = basics[["tconst", "primaryTitle", "originalTitle", "startYear", "genres"]]
    ratings = ratings[["tconst", "averageRating", "numVotes"]]
    principals = principals[["tconst", "nconst", "category"]]
    names = names[["nconst", "primaryName", "primaryProfession"]]

    basics["genres"] = basics["genres"].fillna("").astype(str)

    # =================================================
    # MERGE ENTRE BASICS + RATINGS
    # =================================================
    print("Integrando basics + ratings...")

    merged = basics.merge(ratings, on="tconst", how="left")
    merged["averageRating"] = merged["averageRating"].fillna(0.0)
    merged["numVotes"] = merged["numVotes"].fillna(0).astype(int)

    # =================================================
    # DICCIONARIO: tconst → info completa
    # =================================================
    print("Creando diccionario de títulos...")
    title_dict = merged.set_index("tconst").to_dict(orient="index")

    # =================================================
    # ÍNDICE POR GÉNEROS
    # =================================================
    print("Creando índice por géneros...")
    genre_index = {}

    for tconst, row in merged.set_index("tconst").iterrows():
        for g in row["genres"].split(","):
            if g.strip():
                genre_index.setdefault(g, []).append(tconst)

    # =================================================
    # UNIR PRINCIPALS + NAMES
    # =================================================
    print("Asociando personas con títulos...")

    principals = principals.merge(names, on="nconst", how="left")

    # =================================================
    # DICCIONARIO DE PERSONAS
    # =================================================
    people_dict = {}

    for nconst, row in names.set_index("nconst").iterrows():
        people_dict[nconst] = {
            "name": row["primaryName"],
            "professions": str(row["primaryProfession"]),
            "titles": []
        }

    # Llenar títulos por persona
    for _, row in principals.iterrows():
        nconst = row["nconst"]
        tconst = row["tconst"]
        if nconst in people_dict:
            people_dict[nconst]["titles"].append(tconst)

    # Índice invertido de nombres
    print("Creando índice de nombres...")
    name_index = {}

    for nconst, pdata in people_dict.items():
        nombre = str(pdata["name"]).lower()
        name_index.setdefault(nombre, []).append(nconst)

    # =================================================
    # GUARDAR RESULTADO
    # =================================================
    print("\nGuardando archivo optimizado...")

    optimized_data = {
        "title_dict": title_dict,
        "genre_index": genre_index,
        "people_dict": people_dict,
        "name_index": name_index
    }

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    with open(OUTPUT_PICKLE, "wb") as f:
        pickle.dump(optimized_data, f)

    print("\n✔ Proceso completado.")
    print(f"✔ Archivo generado: {OUTPUT_PICKLE}")


if __name__ == "__main__":
    crear_diccionarios()
