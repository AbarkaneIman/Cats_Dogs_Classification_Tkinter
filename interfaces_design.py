import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from functions import choose_images, extract_colors_from_folder, update_display, train_model, predict_image

selected_image_path = ""  # Globale pour la prédiction

def build_ui(root):
    root.title("Classification Chats vs Chiens")
    root.geometry("800x600")
    root.configure(bg="#F8F8FF")

    # Créer les frames (pages)
    page_selection = tk.Frame(root, bg="#F8F8FF")
    page_prediction = tk.Frame(root, bg="#F8F8FF")

    for frame in (page_selection, page_prediction):
        frame.place(relwidth=1, relheight=1)

    def show_frame(frame):
        frame.tkraise()

    # -------------------- PAGE DE SÉLECTION ET ENTRAÎNEMENT --------------------
    tk.Label(page_selection, text="Projet de Classification : Chats vs Chiens", font=("Arial", 24), bg="#F8F8FF").pack(pady=10)

    frames_container = tk.Frame(page_selection, bg="#F8F8FF")
    frames_container.pack(pady=20)

    # Chats
    chat_container = tk.Frame(frames_container)
    chat_container.grid(row=0, column=0, padx=20)
    cat_frame = tk.Frame(chat_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    cat_frame.pack()
    tk.Button(chat_container, bg="#C2B280", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=5,
              text="Sélectionner des images de chats",
              command=lambda: choose_images("chat", cat_frame, dog_frame)).pack(pady=5)

    # Chiens
    dog_container = tk.Frame(frames_container)
    dog_container.grid(row=0, column=1, padx=20)
    dog_frame = tk.Frame(dog_container, width=300, height=300, bg="white", highlightbackground="black", highlightthickness=2)
    dog_frame.pack()
    tk.Button(dog_container, bg="#C2B280", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=5,
              text="Sélectionner des images de chiens",
              command=lambda: choose_images("chien", cat_frame, dog_frame)).pack(pady=10)

    # Bouton d'entraînement + changement de page
    def train_and_switch():
        train_model()
        show_frame(page_prediction)

    tk.Button(page_selection, text="Entraîner le modèle", font=("Arial", 14), bg="#C2B280", command=train_and_switch).pack(pady=20)

    # -------------------- PAGE DE PRÉDICTION --------------------
    frame_left = tk.Frame(page_prediction, bd=2, relief="groove")
    frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_left, text="Nouvelle photo", font=("Arial", 12)).pack(pady=10)
    img_placeholder = tk.Label(frame_left, text="Chat ou chien", width=20, height=10, bg="white")
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

    tk.Button(frame_left, text="Parcourir", command=browse_image).pack(pady=10)

    frame_right = tk.Frame(page_prediction, bd=2, relief="groove")
    frame_right.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

    tk.Label(frame_right, text="Photo sélectionnée", font=("Arial", 12)).pack(pady=10)
    tk.Label(frame_right, text="Puis cliquer sur prédiction", font=("Arial", 10)).pack(pady=5)

    result_label = tk.Label(frame_right, text="", bg="lightyellow", font=("Arial", 14))
    result_label.pack(pady=20)

    def on_predict_click():
        if selected_image_path:
            result = predict_image(selected_image_path)
            result_label.config(text=result)

    tk.Button(frame_right, text="Prédiction", command=on_predict_click).pack(pady=5)
    tk.Button(page_prediction, text="↩ Retour", command=lambda: show_frame(page_selection)).pack(pady=10)

    # Afficher la première page
    show_frame(page_selection)

    # On retourne la fonction pour usage futur (optionnel)
    return show_frame
