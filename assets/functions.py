import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import random


# Dossiers pour stocker les images de chats et de chiens
CAT_FOLDER="cats_dogs_classification_project/images/cats"

DOG_FOLDER ="cats_dogs_classification_project/images/dogs"

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


# Fonction pour extraire les couleurs dominantes des images dans un dossier
def extract_colors_from_folder(folder_path):
    dominant_colors = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        
        # Vérifier que l'élément est une image avec l'extension appropriée
        if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            dominant_color = extract_dominant_color(img_path)
            dominant_colors.append(dominant_color)
    
    return dominant_colors


# Extraire les couleurs dominantes des images dans le dossier des chats et des chiens
cats_colors = extract_colors_from_folder(CAT_FOLDER)
dogs_colors = extract_colors_from_folder(DOG_FOLDER)


# Afficher les couleurs dominantes extraites
print(f"Couleurs dominantes des chats: {cats_colors}")
print(f"Couleurs dominantes des chiens: {dogs_colors}")


#fonction pour detecter la forme approximative des yeux 
def detect_eye_shapes(folder_path):
    eye_shapes = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Utiliser un classifieur pré-entraîné pour détecter les yeux
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in eyes:
                roi = gray[y:y+h, x:x+w]  # Extraire la région des yeux
                shape = "rond" if w/h < 1.2 else "allongé"  # Forme simple selon le ratio largeur/hauteur
                eye_shapes.append(shape)
                break  # On ne prend qu’un œil par image pour simplifier

    return eye_shapes


# Extraire la forme approximative des yeux depuis des images dans le dossier des chats et des chiens
cat_eye_shapes = detect_eye_shapes(CAT_FOLDER)
dog_eye_shapes = detect_eye_shapes(DOG_FOLDER)

print(f"Formes des yeux des chats : {cat_eye_shapes}")
print(f"Formes des yeux des chiens : {dog_eye_shapes}")


def train_model():
    cats_colors = extract_colors_from_folder(CAT_FOLDER)
    dogs_colors = extract_colors_from_folder(DOG_FOLDER)

    cat_eye_shapes = detect_eye_shapes(CAT_FOLDER)
    dog_eye_shapes = detect_eye_shapes(DOG_FOLDER)

    print(f"Couleurs dominantes des chats: {cats_colors}")
    print(f"Couleurs dominantes des chiens: {dogs_colors}")

    print(f"Formes des yeux des chats : {cat_eye_shapes}")
    print(f"Formes des yeux des chiens : {dog_eye_shapes}")

    messagebox.showinfo("Entraînement terminé", "Les données ont été extraites avec succès !")


    

def fake_predict_image(img_path):
    # Simuler une prédiction aléatoire entre "chat" ou "chien"
    label = random.choice(["chat", "chien"])
    pourcentage = random.randint(50, 99)
    return f"{pourcentage}% {label}"




"""
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
"""