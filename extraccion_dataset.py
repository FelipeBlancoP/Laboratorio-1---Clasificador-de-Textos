# extraccion_dataset.py
import os
from sklearn.datasets import fetch_20newsgroups

# Categorías seleccionadas
categories = [
    "comp.graphics",
    "sci.space", 
    "rec.sport.hockey",
    "talk.politics.mideast",
    "sci.med",
    "alt.atheism"
]

# Crear carpeta raíz donde guardaremos todo
output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

print("Descargando dataset de 20 Newsgroups...")
dataset = fetch_20newsgroups(
    subset="all",
    categories=categories,
    shuffle=True,
    random_state=42,
    remove=()  # Mantener todo el texto original
)

print(f"Dataset descargado: {len(dataset.data)} documentos")

# Guardar cada documento como txt en su carpeta
for i, text in enumerate(dataset.data):
    label = dataset.target_names[dataset.target[i]]
    folder = os.path.join(output_dir, label)
    os.makedirs(folder, exist_ok=True)
    
    filename = os.path.join(folder, f"doc_{i}.txt")
    with open(filename, "w", encoding="utf-8", errors="ignore") as f:
        f.write(text)

print(f"Dataset guardado en la carpeta '{output_dir}'")
print("Estructura creada:")
for category in categories:
    category_path = os.path.join(output_dir, category)
    if os.path.exists(category_path):
        num_files = len([f for f in os.listdir(category_path) if f.endswith('.txt')])
        print(f"  - {category}: {num_files} documentos")