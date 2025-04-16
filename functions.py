import numpy as np
import os
import tkinter as tk
import cv2
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk

# *************************** Dossiers
CAT_FOLDER = "assets/images/cats"
DOG_FOLDER = "assets/images/dogs"

dataset = []
selected_images_chat = []
selected_images_dog = []
cats_colors = []
dogs_colors = []
cat_eye_shapes = []
dog_eye_shapes = []

def create_folders():
    os.makedirs(CAT_FOLDER, exist_ok=True)
    os.makedirs(DOG_FOLDER, exist_ok=True)

def update_display(cat_frame, dog_frame):
    for widget in cat_frame.winfo_children():
        widget.destroy()
    for widget in dog_frame.winfo_children():
        widget.destroy()

    for idx, image_path in enumerate(selected_images_chat):
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        row, col = divmod(idx, 5)
        label = Label(cat_frame, image=photo)
        label.image = photo
        label.grid(row=row, column=col, padx=5, pady=5)

    for idx, image_path in enumerate(selected_images_dog):
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        row, col = divmod(idx, 5)
        label = Label(dog_frame, image=photo)
        label.image = photo
        label.grid(row=row, column=col, padx=5, pady=5)

def choose_images(label, cat_frame, dog_frame):
    files = filedialog.askopenfilenames(title=f"Choisir des images de {label}", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if label == "chat":
        if len(selected_images_chat) + len(files) > 10:
            messagebox.showerror("Erreur", "Max 10 images de chats.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chat"))
            selected_images_chat.append(file)
            img.save(os.path.join(CAT_FOLDER, os.path.basename(file)))
    elif label == "chien":
        if len(selected_images_dog) + len(files) > 10:
            messagebox.showerror("Erreur", "Max 10 images de chiens.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chien"))
            selected_images_dog.append(file)
            img.save(os.path.join(DOG_FOLDER, os.path.basename(file)))
    update_display(cat_frame, dog_frame)

def extract_dominant_color(img_path):
    img = Image.open(img_path).resize((100, 100))
    img_array = np.array(img)
    avg_color = img_array.mean(axis=(0, 1))
    return tuple(avg_color.astype(int))

def extract_colors_from_folder(folder_path):
    return [extract_dominant_color(os.path.join(folder_path, f))
            for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

def detect_eye_shapes(folder_path):
    shapes = []
    for f in os.listdir(folder_path):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, f)
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml').detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in eyes:
                shape = "rond" if w / h < 1.2 else "allongé"
                shapes.append(shape)
                break
    return shapes

def compare_color_distance(dominant_color, reference_colors):
    distances = [np.linalg.norm(np.array(dominant_color) - np.array(c)) for c in reference_colors]
    return min(distances) if distances else float('inf')

def train_model():
    global cats_colors, dogs_colors, cat_eye_shapes, dog_eye_shapes
    cats_colors = extract_colors_from_folder(CAT_FOLDER)
    dogs_colors = extract_colors_from_folder(DOG_FOLDER)
    cat_eye_shapes = detect_eye_shapes(CAT_FOLDER)
    dog_eye_shapes = detect_eye_shapes(DOG_FOLDER)

    print(f"Couleurs chats: {cats_colors}")
    print(f"Couleurs chiens: {dogs_colors}")
    print(f"Yeux chats: {cat_eye_shapes}")
    print(f"Yeux chiens: {dog_eye_shapes}")
    messagebox.showinfo("Entraînement terminé", "Les données ont été extraites avec succès !")

def predict_image(img_path):
    dominant_color = extract_dominant_color(img_path)
    color_distance_cat = compare_color_distance(dominant_color, cats_colors)
    color_distance_dog = compare_color_distance(dominant_color, dogs_colors)

    # Eye shape
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml').detectMultiScale(gray, 1.1, 5)
    eye_shape = "inconnu"
    for (x, y, w, h) in eyes:
        eye_shape = "rond" if w / h < 1.2 else "allongé"
        break

    eye_score_cat = 0 if eye_shape in cat_eye_shapes else 1
    eye_score_dog = 0 if eye_shape in dog_eye_shapes else 1

    # Calcul du score final
    total_score_cat = color_distance_cat + eye_score_cat
    total_score_dog = color_distance_dog + eye_score_dog

    prediction = "chat" if total_score_cat < total_score_dog else "chien"
    messagebox.showinfo("Résultat", f"L'image est probablement un {prediction}.")
