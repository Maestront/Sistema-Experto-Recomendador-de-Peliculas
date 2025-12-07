import pickle

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

        # Obtener título
        title = info.get("primaryTitle") or info.get("originalTitle") or "Unknown"

        # Obtener año
        year = info.get("startYear")
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        elif not isinstance(year, int):
            year = None

        # Normalizar géneros
        raw_genres = info.get("genres", "")
        if isinstance(raw_genres, str):
            genres = [g.strip() for g in raw_genres.split(",") if g.strip()]
        elif isinstance(raw_genres, list):
            genres = raw_genres
        else:
            genres = []

        # Rating real de IMDB
        rating = info.get("averageRating", 0.0)
        try:
            rating = float(rating)
        except:
            rating = 0.0

        # Votos reales de IMDB
        votes = info.get("numVotes", 0)
        try:
            votes = int(votes)
        except:
            votes = 0

        # Crew: opcional, si no existe, lista vacía
        crew = info.get("crew", [])
        if crew is None:
            crew = []

        movies.append({
            "id": tconst,
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

    print("Cargando optimized_data.pkl ...")
    with open("optimized_data.pkl", "rb") as f:
        opt = pickle.load(f)

    print("Claves detectadas:", list(opt.keys()))
    print("Construyendo final_dataset.pkl ...")

    final_data = build_final_dataset(opt)

    with open("final_dataset.pkl", "wb") as f:
        pickle.dump(final_data, f)

    print("✓ final_dataset.pkl generado exitosamente.")
    print(f"Películas en dataset: {len(final_data['movies'])}")
    print(f"Géneros: {len(final_data['genres'])}")
    print(f"Personas: {len(final_data['people'])}")


if __name__ == "__main__":
    main()
