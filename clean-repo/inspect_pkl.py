import pickle

with open("final_dataset.pkl", "rb") as f:
    data = pickle.load(f)

print("=== FINAL DATASET INSPECTION ===\n")

print("Tipo de objeto:", type(data))

if isinstance(data, dict):
    print("\nClaves principales:", list(data.keys()))
else:
    print("\nEl dataset no es un dict. Revisa el archivo.")
    quit()

# Ver contenido específico
title_dict = data.get("title_dict", {})
genre_index = data.get("genre_index", {})
people_dict = data.get("people_dict", {})
name_index = data.get("name_index", {})

print("\nNúmero de títulos:", len(title_dict))
print("Número de géneros:", len(genre_index))
print("Número de personas:", len(people_dict))
print("Número de nombres indexados:", len(name_index))

# Mostrar ejemplos
def print_examples(name, d, n=5):
    print(f"\nEjemplos de {name}:")
    for i, (k, v) in enumerate(d.items()):
        print(" ", k, ":", v)
        if i >= n - 1:
            break

print_examples("title_dict", title_dict)
print_examples("genre_index", genre_index)
print_examples("people_dict", people_dict)
print_examples("name_index", name_index)

print("\n=== FIN ===")
