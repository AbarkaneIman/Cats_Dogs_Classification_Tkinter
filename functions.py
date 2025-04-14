import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Dossiers pour stocker les images de chats et de chiens
CAT_FOLDER = "cats_dogs_classification_project/images/cats"
DOG_FOLDER = "cats_dogs_classification_project/images/dogs"

# Initialiser les listes
dataset = []  # Stocker les données prêtes pour l’entraînement
selected_images_chat = []  # Stocker les chemins des images de chats sélectionnées
selected_images_dog = []   # Stocker les chemins des images de chiens sélectionnées


# Vérifier si les dossiers existent, sinon les créer
def create_folders():
    if not os.path.exists(CAT_FOLDER):
        os.makedirs(CAT_FOLDER)
    if not os.path.exists(DOG_FOLDER):
        os.makedirs(DOG_FOLDER)

from tkinter import Label
from PIL import Image, ImageTk

def update_display(cat_frame, dog_frame):
    # Efface le contenu précédent des frames
    for widget in cat_frame.winfo_children():
        widget.destroy()
    for widget in dog_frame.winfo_children():
        widget.destroy()

    # Affichage des images de chats
    for idx, image_path in enumerate(selected_images_chat):
        img = Image.open(image_path)
        img = img.resize((100, 100))  # Redimensionne l'image
        photo = ImageTk.PhotoImage(img)

        # Calculer la ligne et la colonne pour placer l'image
        row = idx // 5  # 5 images par ligne
        col = idx % 5   # Le reste après division pour déterminer la colonne

        # Crée une label pour afficher l'image
        label = Label(cat_frame, image=photo)
        label.image = photo  # Garder une référence de l'image
        label.grid(row=row, column=col, padx=5, pady=5)

    # Affichage des images de chiens (de façon similaire)
    for idx, image_path in enumerate(selected_images_dog):
        img = Image.open(image_path)
        img = img.resize((100, 100))  # Redimensionne l'image
        photo = ImageTk.PhotoImage(img)

        # Calculer la ligne et la colonne pour placer l'image
        row = idx // 5  # 5 images par ligne
        col = idx % 5   # Le reste après division pour déterminer la colonne

        # Crée une label pour afficher l'image
        label = Label(dog_frame, image=photo)
        label.image = photo  # Garder une référence de l'image
        label.grid(row=row, column=col, padx=5, pady=5)


# Fonction pour choisir les images
def choose_images(label, cat_frame, dog_frame):
    files = filedialog.askopenfilenames(
        title=f"Choisir des images de {label}",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if label == "chat":
        if len(selected_images_chat) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chats.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chat"))
            selected_images_chat.append(file)
            # Copier l'image dans le dossier des chats
            img.save(os.path.join(CAT_FOLDER, os.path.basename(file)))

    elif label == "chien":
        if len(selected_images_dog) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chiens.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chien"))
            selected_images_dog.append(file)
            # Copier l'image dans le dossier des chiens
            img.save(os.path.join(DOG_FOLDER, os.path.basename(file)))

    update_display(cat_frame, dog_frame)




# Fonction pour extraire la couleur dominante 
def extract_dominant_color(img_path):
    img = Image.open(img_path).resize((100, 100))  # Redimensionner l'image à une taille fixe
    img_array = np.array(img)  # Convertir l'image en tableau numpy
    
    # Calculer la couleur dominante (moyenne des couleurs RGB)
    avg_color = img_array.mean(axis=(0, 1))  # Moyenne des pixels en R, G, B
    return tuple(avg_color.astype(int))  # Retourner les valeurs moyennes des couleurs


# Fonction de classification : Classer l'image en chat ou chien basé sur la couleur dominante
def classify_image(img_path, cat_colors, dog_colors):
    dominant_color = extract_dominant_color(img_path)
    
    # Calculer la distance entre la couleur dominante et les couleurs des chats et des chiens
    cat_distances = [np.linalg.norm(np.array(dominant_color) - np.array(c)) for c in cat_colors]
    dog_distances = [np.linalg.norm(np.array(dominant_color) - np.array(d)) for d in dog_colors]
    
    # Trouver la couleur la plus proche parmi les chats et les chiens
    if min(cat_distances) < min(dog_distances):
        return "chat"
    else:
        return "chien"
    


    # Fonction pour entraîner le modèle basé sur les couleurs dominantes
def train_model():
    if len(selected_images_chat) != 10 or len(selected_images_dog) != 10:
        messagebox.showwarning("Incomplet", "Veuillez sélectionner 10 images de chats ET 10 images de chiens.")
        return