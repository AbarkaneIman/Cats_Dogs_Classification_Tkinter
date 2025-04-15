import tkinter as tk
from functions import choose_images, extract_colors_from_folder, update_display, train_model
from functions import fake_predict_image
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def build_ui(root):
    root.geometry("800x600")  # Taille initiale de la fenêtre
    root.minsize(600, 400)    # Taille minimale

    tk.Label(root, text="Projet de Classification : Chats vs Chiens", font=("Arial", 30)).pack(pady=10)

    # Conteneur principal
    frames_container = tk.Frame(root, bg="#F8F8FF")
    frames_container.pack(pady=20)

    # ------- Cadre pour les chats -------
    chat_container = tk.Frame(frames_container)
    chat_container.grid(row=0, column=0, padx=20)

    tk.Button(chat_container, 
                       bg="#C2B280",  # Couleur de fond beige clair
                       fg="white",    # Couleur du texte en blanc
                       font=("Arial", 12, "bold"),  # Police Arial, taille 12, en gras
                       relief="raised",  # Bordure en relief
                       bd=5, text="Sélectionner des images de chats",
                       compound="left",  # Positionne l'image à gauche du texte
                       command=lambda: choose_images("chat", cat_frame, dog_frame)  # Appel de la fonction pour les chats
                       ).pack(pady=5)

    cat_frame = tk.Frame(chat_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    cat_frame.pack()

    # ------- Cadre pour les chiens -------
    dog_container = tk.Frame(frames_container)
    dog_container.grid(row=0, column=1, padx=20)

    tk.Button(dog_container,
                       bg="#C2B280",  # Couleur de fond beige clair
                       fg="white",    # Couleur du texte en blanc
                       font=("Arial", 12, "bold"),  # Police Arial, taille 12, en gras
                       relief="raised",  # Bordure en relief
                       bd=5,  # Épaisseur de la bordure
                       text="Sélectionner des images de chiens",  # Texte du bouton
                       compound="left",  # Positionne l'image à gauche du texte
                       command=lambda: choose_images("chien", cat_frame, dog_frame)  # Appel de la fonction pour les chiens
                       ).pack(pady=10)

    dog_frame = tk.Frame(dog_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    dog_frame.pack()
# ------- Bouton d'entraînement -------
    tk.Button(root, 
          bg="#C2B280", 
          text="Entraîner le modèle", 
          command=train_model)\
          .pack(pady=20)

    # Ce bouton doit appeler une fonction qui va extraire les couleurs des images des chats et des chiens


def on_predict_click():
    if selected_image_path:
        result = fake_predict_image(selected_image_path)
        result_label.config(text=result)


selected_image_path = ""

def build_ui(root):
    root.title("Simulation d'une application IA")
    root.geometry("800x500")

    # Frame gauche
    frame_left = Frame(root, bd=2, relief="groove")
    frame_left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    Label(frame_left, text="Nouvelle photo", font=("Arial", 12)).pack(pady=10)

    img_placeholder = Label(frame_left, text="Chat ou chien ", width=20, height=10, bg="white")
    img_placeholder.pack(pady=10)

    def browse_image():
        global selected_image_path
        selected_image_path = filedialog.askopenfilename()
        if selected_image_path:
            img = Image.open(selected_image_path)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            img_placeholder.config(image=img_tk, text="")
            img_placeholder.image = img_tk

    Button(frame_left, text="Parcourir", command=browse_image).pack(pady=10)

    # Frame droite
    frame_right = Frame(root, bd=2, relief="groove")
    frame_right.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=10)

    Label(frame_right, text="Photo sélectionnée", font=("Arial", 12)).pack(pady=10)
    Label(frame_right, text="puis cliquer sur prédiction", font=("Arial", 10)).pack(pady=5)

    result_label = Label(frame_right, text="", bg="lightyellow", font=("Arial", 14))
    result_label.pack(pady=20)

    def on_predict_click():
        if selected_image_path:
            result = fake_predict_image(selected_image_path)
            result_label.config(text=result)

    Button(frame_right, text="Prédiction", command=on_predict_click).pack(pady=5)