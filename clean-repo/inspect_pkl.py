import pickle

path = r"d:\Documentos (Trabajos)\CETI\7°\SE\Sistema Experto Recomendador de Peliculas\clean-repo\optimized_data.pkl"

with open(path, "rb") as f:
    data = pickle.load(f)

print(type(data))
if isinstance(data, dict):
    print("Claves del archivo:", list(data.keys()))
else:
    print("Contenido:", data)
