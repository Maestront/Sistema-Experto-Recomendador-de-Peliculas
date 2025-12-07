import os
import pandas as pd
import pickle

# Obtener ruta absoluta del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "final_dataset.pkl")

def cargar_dataset():
    with open(DATASET_PATH, "rb") as f:
        df = pickle.load(f)
    return df



# ============================================================
#  CARGA DEL DATASET (DataFrame)
# ============================================================
def cargar_dataset():
    with open(DATASET_PATH, "rb") as f:
        data = pickle.load(f)

    movies = data["movies"]

    df = pd.DataFrame(movies)

    # Asegurar tipos
    df["rating"] = df["rating"].astype(float)
    df["votes"] = df["votes"].astype(int)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Convertir lista de géneros → cadena para filtrar
    df["genres"] = df["genres"].apply(lambda g: ", ".join(g) if isinstance(g, list) else "")

    return df


# ============================================================
#  FILTRO POR PERFIL
# ============================================================
def filtrar_por_perfil(df, perfil):

    if perfil == "mainstream":
        return df[df["votes"] >= 30000]

    elif perfil == "mixed":
        return df[(df["votes"] >= 5000) & (df["votes"] < 30000)]

    elif perfil == "niche":
        return df[df["votes"] < 5000]

    return df


# ============================================================
#  WEIGHTED RATING
# ============================================================
def weighted_rating(row, C=0, M=10000):
    R = row["rating"]
    v = row["votes"]
    return (v / (v + M)) * R + (M / (v + M)) * C


# ============================================================
#  RECOMENDADOR POR GÉNERO
# ============================================================
def recomendar_por_genero(genero, perfil="mixed", n=20):

    df = cargar_dataset()

    # Filtrar por género
    filtrado = df[df["genres"].str.contains(genero, case=False, na=False)]

    if filtrado.empty:
        return f"No se encontraron películas del género '{genero}'."

    # Filtrar por perfil
    filtrado = filtrar_por_perfil(filtrado, perfil)

    if filtrado.empty:
        return f"No hay películas del género '{genero}' para el perfil '{perfil}'."

    # Calcular promedio general C
    C = filtrado["rating"].mean()

    # Calcular weighted rating
    filtrado = filtrado.copy()
    filtrado["wr"] = filtrado.apply(lambda r: weighted_rating(r, C=C), axis=1)

    # Ordenar
    top = filtrado.sort_values("wr", ascending=False).head(n)

    # Formatear salida
    resultados = []
    for _, m in top.iterrows():
        resultados.append(
            f"{m['title']} ({int(m['year']) if not pd.isna(m['year']) else 'N/A'}) "
            f"| WR: {m['wr']:.2f} | Rating: {m['rating']} | Votes: {m['votes']} | Géneros: {m['genres']}"
        )

    return "\n".join(resultados)


# ============================================================
#  TEST AUTOMÁTICO
# ============================================================
if __name__ == "__main__":
    print("=== TEST: Acción (mixed) ===")
    print(recomendar_por_genero("Action", perfil="mixed"))
