import tkinter as tk
from functions import choose_images, update_display, train_model
def build_ui(root):
    root.geometry("800x600")  # Taille initiale de la fenêtre
    root.minsize(600, 400)    # Taille minimale

    tk.Label(root, text="Projet de Classification : Chats vs Chiens", font=("Arial", 16)).pack(pady=10)

    # Conteneur principal
    frames_container = tk.Frame(root)
    frames_container.pack()

    # ------- Cadre pour les chats -------
    chat_container = tk.Frame(frames_container)
    chat_container.grid(row=0, column=0, padx=20)

    tk.Button(chat_container, text="Sélectionner des images de chats",
              command=lambda: choose_images("chat", cat_frame, dog_frame)).pack(pady=5)

    cat_frame = tk.Frame(chat_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    cat_frame.pack()

    # ------- Cadre pour les chiens -------
    dog_container = tk.Frame(frames_container)
    dog_container.grid(row=0, column=1, padx=20)

    tk.Button(dog_container, text="Sélectionner des images de chiens",
              command=lambda: choose_images("chien", cat_frame, dog_frame)).pack(pady=5)

    dog_frame = tk.Frame(dog_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    dog_frame.pack()

    # ------- Bouton d'entraînement -------
    tk.Button(root, text="Entraîner le modèle", command=train_model).pack(pady=20)
