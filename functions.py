from tkinter import filedialog
from PIL import Image
import numpy as np

# Fonction pour choisir les images
def choose_images(label, dataset):
    images = []
    for _ in range(10):
        file = filedialog.askopenfilename(title=f"Choisir une image de {label}", filetypes=[("Image Files", "*.jpg;*.png")])
        if file:
            img = Image.open(file)
            img = img.resize((100, 100))  # Redimensionner l'image
            img_array = np.array(img)  # Convertir en tableau numpy
            images.append((img_array.flatten(), label))  # Ajouter l'image et l'étiquette
    dataset.extend(images)

# Fonction d'entraînement (Simuler le processus)
def train_model(dataset):
    # On considère que l'entraînement a simplement constitué de stocker les données
    return dataset

# Fonction pour tester une image
def test_image(test_image_path, dataset):
    test_img = Image.open(test_image_path).resize((100, 100))
    test_img_array = np.array(test_img).flatten()

    # Comparer avec les images du dataset
    best_match = None
    best_score = float('inf')  # On cherche la plus petite différence

    for img_array, label in dataset:
        score = np.linalg.norm(test_img_array - img_array)  # Calcul de la distance euclidienne
        if score < best_score:
            best_score = score
            best_match = label

    # Retourne l'étiquette la plus proche
    return best_match

# Ajoute cette fonction dans ton code principal `main.py`

"""
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Fonction pour choisir des images
def choose_images(label):
    file_paths = filedialog.askopenfilenames(title=f"Choisir des images de {label}", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    image_list = []
    for path in file_paths:
        img = Image.open(path)
        img = img.resize((100, 100))  # Redimensionner l'image
        img_array = np.array(img).flatten()  # Transformer l'image en vecteur
        image_list.append((img_array, label))  # Ajouter l'image et son étiquette
    return image_list

# Fenêtre principale
root = tk.Tk()
root.title("Création du dataset")

# Boutons pour choisir des images de chats et de chiens
chat_button = tk.Button(root, text="Choisir des images de chats", command=lambda: choose_images("chat"))
chat_button.pack(pady=10)

dog_button = tk.Button(root, text="Choisir des images de chiens", command=lambda: choose_images("chien"))
dog_button.pack(pady=10)

root.mainloop()
"""