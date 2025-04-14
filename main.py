import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from utils import add_to_dataset, train_model, predict_image, calculate_dataset_accuracy

class IAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation d'une application IA")
        self.root.geometry("900x600")

        self.tabControl = ttk.Notebook(root)

        # Tabs
        self.train_tab = ttk.Frame(self.tabControl)
        self.test_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.train_tab, text='Entraînement')
        self.tabControl.add(self.test_tab, text='Test')
        self.tabControl.pack(expand=1, fill="both")

        self.chat_images = []
        self.chien_images = []

        self.build_train_tab()
        self.build_test_tab()

    def build_train_tab(self):
        left_frame = tk.Frame(self.train_tab, width=200)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="Dataset", font=("Arial", 12)).pack(pady=5)
        # icons
        for _ in range(6):
            img = tk.Label(left_frame, text="🐶🐱", font=("Arial", 18))
            img.pack(pady=5)

        right_frame = tk.Frame(self.train_tab)
        right_frame.pack(side="right", expand=True, padx=10, pady=10)

        # Chat images
        tk.Label(right_frame, text="Sélectionner 10 images de chats").pack()
        self.chat_frame = tk.Frame(right_frame)
        self.chat_frame.pack()
        self.chat_buttons = [self.create_image_slot(self.chat_frame, "chat") for _ in range(10)]

        # Chien images
        tk.Label(right_frame, text="Sélectionner 10 images de chien").pack(pady=(10, 0))
        self.chien_frame = tk.Frame(right_frame)
        self.chien_frame.pack()
        self.chien_buttons = [self.create_image_slot(self.chien_frame, "chien") for _ in range(10)]

        self.train_button = tk.Button(right_frame, text="Entraîner", command=self.train)
        self.train_button.pack(pady=10)

    def create_image_slot(self, parent, label):
        slot = tk.Label(parent, width=10, height=5, relief="ridge", bd=2)
        slot.pack(side="left", padx=2, pady=2)
        slot.bind("<Button-1>", lambda e: self.select_image(slot, label))
        return slot

    def select_image(self, slot, label):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path).resize((50, 50))
            tk_img = ImageTk.PhotoImage(img)
            slot.image = tk_img
            slot.config(image=tk_img)
            add_to_dataset(file_path, label)

    def train(self):
        success = train_model()
        if success:
            messagebox.showinfo("Succès", "Modèle entraîné avec succès !")
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'entraînement")

    def build_test_tab(self):
        instruction = tk.Label(self.test_tab, text="(1) Sélectionner une nouvelle photo\n(2) Cliquer sur Prédiction\n(3) Voir le résultat", justify="left")
        instruction.pack(anchor="nw", padx=20, pady=10)

        frame = tk.Frame(self.test_tab)
        frame.pack(padx=20, pady=10)

        # Section gauche
        left = tk.Frame(frame)
        left.pack(side="left", padx=20)

        tk.Label(left, text="Nouvelle photo").pack()
        self.btn_browse = tk.Button(left, text="Parcourir", command=self.choose_test_image)
        self.btn_browse.pack(pady=10)
        self.selected_img_path = None

        # Section droite
        right = tk.Frame(frame)
        right.pack(side="left", padx=20)

        tk.Label(right, text="Photo sélectionnée").pack()
        self.img_preview = tk.Label(right)
        self.img_preview.pack(pady=5)

        self.predict_button = tk.Button(right, text="Prédiction", command=self.predict)
        self.predict_button.pack(pady=5)

        self.result_label = tk.Label(right, text="", bg="#fdf5d7", font=("Arial", 16), width=20)
        self.result_label.pack(pady=5)

    def choose_test_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_img_path = file_path
            img = Image.open(file_path).resize((100, 100))
            tk_img = ImageTk.PhotoImage(img)
            self.img_preview.image = tk_img
            self.img_preview.config(image=tk_img)

    def predict(self):
        if self.selected_img_path:
            label, confidence = predict_image(self.selected_img_path)
            self.result_label.config(text=f"{confidence}% {label}")
        else:
            messagebox.showwarning("Attention", "Veuillez choisir une image d'abord.")

if __name__ == "__main__":
    root = tk.Tk()
    app = IAApp(root)
    root.mainloop()
