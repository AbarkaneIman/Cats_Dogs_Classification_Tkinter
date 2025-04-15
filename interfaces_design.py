import tkinter as tk
from PIL import Image, ImageTk
from functions import choose_images, train_model, predict_image
from tkinter import filedialog

def build_ui(root):
    root.geometry("900x700")
    root.minsize(700, 500)
    root.configure(bg="#f7f9fc")

    # Titre
    tk.Label(
        root,
        text="🐾 Projet de Classification : Chats vs Chiens 🐾",
        font=("Segoe UI", 26, "bold"),
        bg="#f7f9fc",
        fg="#2c3e50"
    ).pack(pady=20)

    # Conteneur principal
    frames_container = tk.Frame(root, bg="#f7f9fc")
    frames_container.pack(pady=20)

    # Cadre images chats
    chat_container = tk.Frame(frames_container, bg="#f7f9fc")
    chat_container.grid(row=0, column=0, padx=30)

    tk.Label(
        chat_container,
        text="Images de chats",
        font=("Segoe UI", 12, "bold"),
        bg="#f7f9fc",
        fg="#34495e"
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

    # Cadre images chiens
    dog_container = tk.Frame(frames_container, bg="#f7f9fc")
    dog_container.grid(row=0, column=1, padx=30)

    tk.Label(
        dog_container,
        text="Images de chiens",
        font=("Segoe UI", 12, "bold"),
        bg="#f7f9fc",
        fg="#34495e"
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

    # Bouton entraînement
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

    # Cadre pour la prédiction
    prediction_frame = tk.Frame(root, bg="#f7f9fc")
    prediction_frame.pack(pady=20)

    result_label = tk.Label(
        prediction_frame,
        text="",
        font=("Segoe UI", 14, "bold"),
        bg="#f7f9fc",
        fg="#2d3436"
    )
    result_label.pack(pady=10)

    image_label = tk.Label(prediction_frame, bg="#f7f9fc")
    image_label.pack()

    def handle_prediction():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            # Afficher l'image
            img = Image.open(file_path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            image_label.configure(image=photo)
            image_label.image = photo  # garder référence

            # Faire la prédiction
            result = predict_image(file_path)
            result_label.config(text=result)

    tk.Button(
        root,
        text="🔍 Prédire une nouvelle image",
        bg="#8e44ad",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        command=handle_prediction
    ).pack(pady=20)
