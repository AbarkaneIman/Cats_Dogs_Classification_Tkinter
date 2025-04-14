import numpy as np
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

        
# Fonction pour mettre à jour l'affichage
def update_display(cat_frame, dog_frame):
    for widget in cat_frame.winfo_children():
        widget.destroy()
    for widget in dog_frame.winfo_children():
        widget.destroy()

    # Affichage des chats
    for idx, image_path in enumerate(selected_images_chat):
        img = Image.open(image_path)
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(cat_frame, image=photo)
        label.image = photo
        label.grid(row=idx, column=0, padx=5, pady=5)

    # Affichage des chiens
    for idx, image_path in enumerate(selected_images_dog):
        img = Image.open(image_path)
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(dog_frame, image=photo)
        label.image = photo
        label.grid(row=idx, column=0, padx=5, pady=5)

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

    elif label == "chien":
        if len(selected_images_dog) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chiens.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chien"))
            selected_images_dog.append(file)

    update_display(cat_frame, dog_frame)

# Fonction pour entraîner le modèle
def train_model():
    if len(selected_images_chat) != 10 or len(selected_images_dog) != 10:
        messagebox.showwarning("Incomplet", "Veuillez sélectionner 10 images de chats ET 10 images de chiens.")
        return
    messagebox.showinfo("Modèle", "Le modèle est entraîné avec succès 🎉 (simulation).")


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