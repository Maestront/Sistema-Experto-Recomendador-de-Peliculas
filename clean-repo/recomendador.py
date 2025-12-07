import pickle
import numpy as np

# ============================================================
#  CARGA DE DATASET
# ============================================================
print("Cargando final_dataset.pkl ...")

with open("final_dataset.pkl", "rb") as f:
    data = pickle.load(f)

movies = data["movies"]

print("Películas cargadas:", len(movies))


# ============================================================
#  DIAGNÓSTICO DE RATINGS
# ============================================================
ratings = [m["rating"] for m in movies if m["rating"] is not None]
valid = [r for r in ratings if 0 <= r <= 10]

print("\n=== DIAGNÓSTICO DE RATINGS ===")
print("Ratings totales analizados:", len(ratings))
print("Ratings válidos (0–10):", len(valid))
print("Rating mínimo encontrado:", min(valid))
print("Rating máximo encontrado:", max(valid))
unique_r = sorted(set(valid))[:20]
print("Ejemplos de ratings únicos:", unique_r)


# ============================================================
#  FILTRO POR GÉNERO
# ============================================================
TARGET_GENRE = "Action"
movies = [m for m in movies if TARGET_GENRE in m["genres"]]

print("Películas disponibles:", len(movies))


# ============================================================
#  CONFIGURACIÓN SISTEMA HÍBRIDO
# ============================================================
N_RECOMMENDATIONS = 20

# Porcentajes automáticos
PCT_MAINSTREAM = 0.50
PCT_MIXED = 0.20
PCT_NICHE = 0.30

# Weighted Rating
M = 10000
C = np.mean([m["rating"] for m in movies])


def weighted_rating(m, C=C, M=M):
    R = m["rating"]
    v = m["votes"] if m["votes"] else 0
    return (v / (v + M)) * R + (M / (v + M)) * C


# ============================================================
#  SEGMENTACIÓN AUTOMÁTICA POR PERCENTILES DE VOTOS
# ============================================================
votes = np.array([m["votes"] for m in movies])
p80 = np.percentile(votes, 80)
p30 = np.percentile(votes, 30)

mainstream = []
mixed = []
niche = []

for m in movies:
    v = m["votes"]
    if v >= p80:
        mainstream.append(m)
    elif v >= p30:
        mixed.append(m)
    else:
        niche.append(m)

print("Segmentos generados:")
print("  Mainstream:", len(mainstream))
print("  Mixed:", len(mixed))
print("  Niche:", len(niche))


# ============================================================
#  ORDENAR CADA SEGMENTO POR WEIGHTED RATING
# ============================================================
mainstream.sort(key=lambda x: weighted_rating(x), reverse=True)
mixed.sort(key=lambda x: weighted_rating(x), reverse=True)
niche.sort(key=lambda x: weighted_rating(x), reverse=True)


# ============================================================
#  SELECCIÓN FINAL
# ============================================================
n_main = int(N_RECOMMENDATIONS * PCT_MAINSTREAM)
n_mix = int(N_RECOMMENDATIONS * PCT_MIXED)
n_nich = N_RECOMMENDATIONS - n_main - n_mix

final_list = mainstream[:n_main] + mixed[:n_mix] + niche[:n_nich]


# ============================================================
#  MOSTRAR RESULTADOS
# ============================================================
print("\n=== RECOMENDACIONES ===")
for m in final_list:
    wr = weighted_rating(m)
    print(
        f"{m['title']} ({m['year']}) | WR: {wr:.2f} | "
        f"Rating: {m['rating']} | Votes: {m['votes']} | "
        f"Géneros: {', '.join(m['genres'])}"
    )
