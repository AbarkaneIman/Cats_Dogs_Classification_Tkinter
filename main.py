"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# Initialiser les listes
dataset = [] #Stocker les données prêtes pour l’entraînement
selected_images_chat = []  #Stocker les chemins des images de chats sélectionnées
selected_images_dog = []   #Stocker les chemins des images de chiens sélectionnées

# Fenêtre principale
root = tk.Tk()    #Créer la fenêtre principale
root.title("Classification Chats vs Chiens")   #Donner un nom visible à la fenêtre de l'application

# Fonctions
def update_display():
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

def choose_images(label):
    files = filedialog.askopenfilenames(  #Ouvre une boîte de dialogue pour sélectionner plusieurs images
        title=f"Choisir des images de {label}",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if label == "chat":
        if len(selected_images_chat) + len(files) > 10: #Si oui → affiche un message d’erreur
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chats.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))  #Ouvre et redimensionne chaque image
            dataset.append((np.array(img).flatten(), "chat"))  #ransforme l'image en vecteur (pour un futur modèle)
            selected_images_chat.append(file)

    elif label == "chien":
        if len(selected_images_dog) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chiens.")
            return
        for file in files:
            img = Image.open(file).resize((100, 100))
            dataset.append((np.array(img).flatten(), "chien")) #	Stocke l’image + son label
            selected_images_dog.append(file) #Liste des chemins d’images pour l’affichage graphique

    update_display() #Rafraîchit l’affichage dans l’interface Tkinter

def train_model():
    if len(selected_images_chat) != 10 or len(selected_images_dog) != 10:
        messagebox.showwarning("Incomplet", "Veuillez sélectionner 10 images de chats ET 10 images de chiens.")
        return
    messagebox.showinfo("Modèle", "Le modèle est entraîné avec succès 🎉 (simulation).")

# Interface
tk.Label(root, text="Projet de Classification : Chats vs Chiens", font=("Arial", 16)).pack(pady=10)

frames_container = tk.Frame(root)
frames_container.pack()

cat_frame = tk.LabelFrame(frames_container, text="Chats", padx=10, pady=10)
cat_frame.grid(row=0, column=0, padx=10)

dog_frame = tk.LabelFrame(frames_container, text="Chiens", padx=10, pady=10)
dog_frame.grid(row=0, column=1, padx=10)

btns = tk.Frame(root)
btns.pack(pady=10)

tk.Button(btns, text="Sélectionner des images de chats", command=lambda: choose_images("chat")).grid(row=0, column=0, padx=10)
tk.Button(btns, text="Sélectionner des images de chiens", command=lambda: choose_images("chien")).grid(row=0, column=1, padx=10)

tk.Button(root, text="Entraîner le modèle", command=train_model).pack(pady=20)

root.mainloop()
"""
import tkinter as tk
from interfaces_design import build_ui

root = tk.Tk()
root.title("Classification Chats vs Chiens")

# Définir les dimensions initiales (par exemple 800x600)
root.geometry("800x600")

# Construction de l'interface
build_ui(root)

root.mainloop()
