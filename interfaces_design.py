import tkinter as tk
from functions import choose_images, train_model

def build_ui(root):
    root.geometry("900x600")
    root.minsize(700, 500)
    root.configure(bg="#f7f9fc")  # Fond doux

    # Titre
    tk.Label(
        root,
        text="🐾 Projet de Classification : Chats vs Chiens 🐾",
        font=("Segoe UI", 26, "bold"),
        bg="#f7f9fc",
        fg="#2c3e50"
    ).pack(pady=20)

    # Conteneur principal pour les cadres de sélection
    frames_container = tk.Frame(root, bg="#f7f9fc")
    frames_container.pack(pady=20)

    # ------ Cadre pour les images de chats ------
    chat_container = tk.Frame(frames_container, bg="#f7f9fc")
    chat_container.grid(row=0, column=0, padx=30)

    tk.Label(
        chat_container,
        text="Images de chats",
        font=("Segoe UI", 12, "bold"),
        bg="#f7f9fc",
        fg="#34495e"
    ).pack(pady=5)

    tk.Button(
        chat_container,
        text="📁 Sélectionner des images de chats",
        bg="#2f80ed",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        command=lambda: choose_images("chat", cat_frame, dog_frame)
    ).pack(pady=5)

    cat_frame = tk.Frame(
        chat_container,
        width=300,
        height=300,
        bg="white",
        highlightbackground="#dcdde1",
        highlightthickness=2
    )
    cat_frame.pack()
    tk.Button(chat_container, bg="#C2B280", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=5,
              text="Sélectionner des images de chats",
              command=lambda: choose_images("chat", cat_frame, dog_frame)).pack(pady=5)

    # ------ Cadre pour les images de chiens ------
    dog_container = tk.Frame(frames_container, bg="#f7f9fc")
    dog_container.grid(row=0, column=1, padx=30)

    tk.Label(
        dog_container,
        text="Images de chiens",
        font=("Segoe UI", 12, "bold"),
        bg="#f7f9fc",
        fg="#34495e"
    ).pack(pady=5)

    tk.Button(
        dog_container,
        text="📁 Sélectionner des images de chiens",
        bg="#2f80ed",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        command=lambda: choose_images("chien", cat_frame, dog_frame)
    ).pack(pady=5)

    dog_frame = tk.Frame(
        dog_container,
        width=300,
        height=300,
        bg="white",
        highlightbackground="#dcdde1",
        highlightthickness=2
    )
    dog_frame.pack()

    # ------ Bouton d'entraînement ------
    tk.Button(
        root,
        text="🚀 Entraîner le modèle",
        bg="#27ae60",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        command=train_model
    ).pack(pady=30)
