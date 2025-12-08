import pickle
import os

# ==========================
#  RUTAS ABSOLUTAS
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

INPUT_PICKLE = os.path.join(PROCESSED_DIR, "optimized_data.pkl")
OUTPUT_PICKLE = os.path.join(PROCESSED_DIR, "final_dataset.pkl")


def build_final_dataset(opt):
    """
    Convierte optimized_data.pkl (title_dict, people_dict, etc.)
    en un dataset final listo para búsquedas y recomendaciones.
    """

    title_dict = opt["title_dict"]
    people_dict = opt["people_dict"]
    genre_index = opt["genre_index"]
    name_index = opt["name_index"]

    movies = []

    for tconst, info in title_dict.items():

        title = info.get("primaryTitle") or info.get("originalTitle") or "Unknown"

        # Año
        year = info.get("startYear")
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        elif not isinstance(year, int):
            year = None

        # Normalización de géneros
        raw_genres = info.get("genres", "")
        genres = [g.strip() for g in raw_genres.split(",") if g.strip()] \
            if isinstance(raw_genres, str) else []

        # Ratings
        rating = float(info.get("averageRating", 0.0))
        votes = int(info.get("numVotes", 0))

        # Crew
        crew = info.get("crew", []) or []

        movies.append({
            # *** CORRECCIÓN CRÍTICA: Cambiamos 'id' por 'tconst' ***
            "tconst": tconst, 
            "title": title,
            "year": year,
            "genres": genres,
            "rating": rating,
            "votes": votes,
            "crew": crew
        })

    final_data = {
        "movies": movies,
        "genres": genre_index,
        "people": people_dict,
        "name_index": name_index
    }

    return final_data


def main():
    print("=== BUILD FINAL DATASET ===")

    print(f"Cargando {INPUT_PICKLE} ...")

    with open(INPUT_PICKLE, "rb") as f:
        opt = pickle.load(f)

    print("Claves detectadas:", list(opt.keys()))
    print(f"Construyendo {OUTPUT_PICKLE} ...")

    final_data = build_final_dataset(opt)

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    with open(OUTPUT_PICKLE, "wb") as f:
        pickle.dump(final_data, f)

    print("✓ final_dataset.pkl generado exitosamente.")
    print(f"Películas en dataset: {len(final_data['movies'])}")
    print(f"Géneros: {len(final_data['genres'])}")
    print(f"Personas: {len(final_data['people'])}")


if __name__ == "__main__":
    main()
