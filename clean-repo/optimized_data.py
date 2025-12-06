import pickle
import pandas as pd

# Rutas
OPTIMIZED_PATH = r"D:\Documentos (Trabajos)\CETI\7°\SE\Sistema Experto Recomendador de Peliculas\clean-repo\optimized_data.pkl"
FINAL_DATASET_PATH = r"D:\Documentos (Trabajos)\CETI\7°\SE\Sistema Experto Recomendador de Peliculas\clean-repo\final_dataset.pkl"

# Cargar optimized_data
with open(OPTIMIZED_PATH, "rb") as f:
    optimized_data = pickle.load(f)

# title_dict → basics + ratings
titles = pd.DataFrame.from_dict(optimized_data["title_dict"], orient="index")

# people_dict → información de personas
people = pd.DataFrame.from_dict(optimized_data["people_dict"], orient="index")

# genre_index y name_index se pueden guardar tal cual como dicts
genre_index = optimized_data["genre_index"]
name_index = optimized_data["name_index"]

# Construir dataset final como un dict
final_dataset = {
    "titles": titles,
    "people": people,
    "genre_index": genre_index,
    "name_index": name_index
}

# Guardar final_dataset.pkl
with open(FINAL_DATASET_PATH, "wb") as f:
    pickle.dump(final_dataset, f)

print("final_dataset.pkl generado correctamente, listo para el recomendador.")
