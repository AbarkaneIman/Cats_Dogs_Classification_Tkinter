import tkinter as tk
from interfaces_design import build_ui  # Assure-toi que cette fonction est bien définie
from functions import create_folders  # Facultatif, à utiliser si besoin

# Créer la fenêtre principale
root = tk.Tk()
root.title("Classification Chats vs Chiens")
root.geometry("800x600")
root.configure(bg="#F8F8FF")  # Couleur de fond

# Construire l'interface (définie dans interfaces_design.py)
build_ui(root)

# Lancer la boucle principale Tkinter
root.mainloop()
