import numpy as np
import os
import tkinter as tk
import cv2
import random
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk


# ***************************Dossiers pour stocker les images de chats et de chiens
CAT_FOLDER="assets/images/cats"
DOG_FOLDER ="assets/images/dogs"


# ***************Initialiser les listes
dataset = []  # Stocker les données prêtes pour l’entraînement
selected_images_chat = []  # Stocker les chemins des images de chats sélectionnées
selected_images_chien = []   # Stocker les chemins des images de chiens sélectionnées

#************************** Vérifier si les dossiers existent, sinon les créer
def create_folders():
    if not os.path.exists(CAT_FOLDER):
        os.makedirs(CAT_FOLDER)
    if not os.path.exists(DOG_FOLDER):
        os.makedirs(DOG_FOLDER)

#************************ fonction qui affiche les images dans les frames 
def update_display(cat_frame, dog_frame):
    # Efface le contenu précédent des frames
    for widget in cat_frame.winfo_children():
        widget.destroy()
    for widget in dog_frame.winfo_children():
        widget.destroy()

    # Affichage des images de chats
    for idx, image_path in enumerate(selected_images_chat):
        img = Image.open(image_path) #ouvrir l'image selctionne
        img = img.resize((150, 150))  # Redimensionne l'image
        photo = ImageTk.PhotoImage(img) #convertit l'image en un format compatible avec Tkinter

        # Calculer la ligne et la colonne pour placer l'image
        row = idx // 5  # 5 images par ligne
        col = idx % 5   # Le reste après division pour déterminer la colonne

        # Crée une label pour afficher l'image
        label = Label(cat_frame, image=photo)
        label.image = photo  # Garder une référence de l'image
        label.grid(row=row, column=col, padx=5, pady=5)# place le label contenant l'image dans la grille à la position calculée

    # Affichage des images de chiens (de façon similaire)
    for idx, image_path in enumerate(selected_images_chien):
        img = Image.open(image_path)
        img = img.resize((150, 150))  # Redimensionne l'image
        photo = ImageTk.PhotoImage(img)
        # Calculer la ligne et la colonne pour placer l'image
        row = idx // 5  # 5 images par ligne
        col = idx % 5   # Le reste après division pour déterminer la colonne

        # Crée une label pour afficher l'image
        label = Label(dog_frame, image=photo)
        label.image = photo  # Garder une référence de l'image
        label.grid(row=row, column=col, padx=5, pady=5)

# **********************************Fonction pour choisir les images
def choose_images(label, cat_frame, dog_frame):
    files = filedialog.askopenfilenames(#ouvre une boîte de dialogue permettant à l'utilisateur de sélectionner plusieurs fichiers.
        title=f"Choisir des images de {label}", # le titre de la fenêtre
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")] # les types de images acceptés, 
    )

    if label == "chat":
        if len(selected_images_chat) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chats.")
            return
        for file in files:
            img = Image.open(file).resize((150, 150)) 
            dataset.append((np.array(img).flatten(), "chat"))#image convertie en un tableau NumPy ettransforme en vecteur et enregistr dans dataset dataset avec l'étiquette "chat"
            selected_images_chat.append(file)#chemin de l'image est ajouté à la liste selected_images_chat, pour garder une trace des images sélectionnées.
            # Copier l'image dans le dossier des chats
            img.save(os.path.join(CAT_FOLDER, os.path.basename(file)))#L'image est copiée dans un dossier CAT_FOLDER

    elif label == "chien":
        if len(selected_images_chien) + len(files) > 10:
            messagebox.showerror("Erreur", "Vous ne pouvez sélectionner que 10 images de chiens.")
            return
        for file in files:
            img = Image.open(file).resize((150, 150)) 
            dataset.append((np.array(img).flatten(), "chien"))
            selected_images_chien.append(file)
            # Copier l'image dans le dossier des chiens
            img.save(os.path.join(DOG_FOLDER, os.path.basename(file)))#save seulement la partie contient le nom de l image dans fichier

    update_display(cat_frame, dog_frame)


#****************** Fonction pour extraire la couleur dominante
def extract_dominant_color(img_path):
    img = Image.open(img_path).resize((150, 150))   # Redimensionner l'image à une taille fixe
    img_array = np.array(img)  # Convertir l'image en tableau numpy
    
    # Calculer la couleur dominante (moyenne des couleurs RGB)
    avg_color = img_array.mean(axis=(0, 1))  # Moyenne des pixels en R, G, B
    # Retourner la couleur dominante sous la forme d'une chaîne lisible
    return f"RGB({int(avg_color[0])}, {int(avg_color[1])}, {int(avg_color[2])})"

# ******************** Fonction pour extraire les couleurs dominantes d'une liste d'images avec un label
def extract_colors_from_images(image_list, label):

    dominant_colors = []  # Liste pour stocker les couleurs dominantes
    for img_path in image_list:
        dominant_color = extract_dominant_color(img_path)  # Extraire la couleur dominante de l'image
        dominant_colors.append((label, dominant_color))  # Ajouter la couleur dominante avec le label
        
    return dominant_colors  # Retourner la liste des couleurs dominantes avec le label

# Exemple d'utilisation pour les images de chats et de chiens
cats_colors = extract_colors_from_images(selected_images_chat, "chat")
dogs_colors = extract_colors_from_images(selected_images_chien, "chien")


# *********************************Afficher les couleurs dominantes extraites
print(f"Couleurs dominantes des chats: {cats_colors}")
print(f"Couleurs dominantes des chiens: {dogs_colors}")



#*******************************fonction pour detecter la forme approximative des yeux 

def detect_eye_shapes(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"{image_path}: image introuvable.")
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+int(h*0.6), x:x+w]  # se concentrer sur le haut du visage
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.05, minNeighbors=3, minSize=(10, 10))

        if len(eyes) > 0:
            print(f"{image_path}: {len(eyes)} yeux détectés")
            return len(eyes)

    print(f"{image_path}: Aucun œil détecté")
    return None
   
#*******************************Fonction pour parcourir une liste d'images et détecter la forme des yeux
def detect_eye_shapes_from_liste(liste):
    all_eye_shapes = {}  # Dictionnaire pour stocker les formes des yeux pour chaque image

    for img_path in liste:
        eye_shapes = detect_eye_shapes(img_path)  # Appeler la fonction de détection pour chaque image
        all_eye_shapes[img_path] = eye_shapes  # Ajouter les formes des yeux dans le dictionnaire

    return all_eye_shapes


# *****************************Extraire la forme approximative des yeux depuis des images dans le dossier des chats et des chiens
cat_eye_shapes =  detect_eye_shapes_from_liste(selected_images_chat)
dog_eye_shapes =  detect_eye_shapes_from_liste(selected_images_chien)

print(f"Formes des yeux des chats : {cat_eye_shapes}")
print(f"Formes des yeux des chiens : {dog_eye_shapes}")

#fonction pour estimer la taille d un animal depuis une image
def estimer_taille_animal(image_path):
    # Charger l'image en niveaux de gris
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Appliquer un flou pour enlever du bruit
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # Détection des contours
    _, threshold = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Trouver les contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Trouver le plus grand contour (supposé être l'animal)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        animal_area = cv2.contourArea(largest_contour)
    else:
        animal_area = 0
    # Taille totale de l'image
    total_area = image.shape[0] * image.shape[1]
    # Proportion de l’image occupée par l’animal
    taille_relative = animal_area / total_area
    return taille_relative

#******************fonction parcourir la lsite des images 
def estimer_taille_liste(liste):
    tailles_relatives = []  # Liste pour stocker les tailles relatives

    for path in liste:
        taille = estimer_taille_animal(path)  # Appliquer la fonction à chaque image
        tailles_relatives.append(taille)      # Ajouter le résultat à la liste

    return tailles_relatives

#******estimer les tailles relatives des chats et des chiens
cats_relatives_tailles =estimer_taille_liste(selected_images_chat)
dogs_relatives_tailles =estimer_taille_liste(selected_images_chien)
 
#*****fonction pour detecter la forme des ooreilles
def detect_ear_shape(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sharp_points = 0

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            x, y, w, h = cv2.boundingRect(cnt)
            if y < img.shape[0] // 2:  # Partie haute
                sharp_points += 1

    if sharp_points >= 2:
        return "pointues"
    else:
        return "arrondies"

        #****fonction pour parcourir la liste des chat et chien
    
def detect_ear_shapes_from_list(image_list):
    resultats = {}  # Dictionnaire pour stocker les résultats

    for image_path in image_list:
        forme = detect_ear_shape(image_path)
        resultats[image_path] = forme

    return resultats

cats_ears_shapes=detect_ear_shapes_from_list(selected_images_chat)
dogs_ears_shapes=detect_ear_shapes_from_list(selected_images_chien)
    


def train_model():
    # Exemple d'utilisation pour les images de chats et de chiens
    cats_colors = extract_colors_from_images(selected_images_chat, "chat")
    dogs_colors = extract_colors_from_images(selected_images_chien, "chien")

    cat_eye_shapes = detect_eye_shapes_from_liste(selected_images_chat)
    dog_eye_shapes = detect_eye_shapes_from_liste(selected_images_chien)

    cats_relatives_tailles = estimer_taille_liste(selected_images_chat)
    dogs_relatives_tailles = estimer_taille_liste(selected_images_chien)

    cats_ears_shapes = detect_ear_shapes_from_list(selected_images_chat)
    dogs_ears_shapes = detect_ear_shapes_from_list(selected_images_chien)
   # afficher_couleurs_dominantes(couleurs_chats, couleurs_chiens):
    print("Couleurs dominantes des chats :")
    for couleur in cats_colors:
        print(f"{couleur[0]} - {couleur[1]}")
    
    print("\nCouleurs dominantes des chiens :")
    for couleur in dogs_colors:
        print(f"{couleur[0]} - {couleur[1]}")

    

    #afficher_formes_yeux(yeux_chats, yeux_chiens):
    print("Formes des yeux des chats :")
    for img, forme in cat_eye_shapes.items():
        print(f"{img}: {forme}")
    
    print("\nFormes des yeux des chiens :")
    for img, forme in dog_eye_shapes.items():
        print(f"{img}: {forme}")

    #afficher_tailles_relatives(tailles_chats, tailles_chiens):
    print("Taille relative des chats :")
    for taille in cats_relatives_tailles:
        print(f"{taille:.2f}")
    
    print("\nTaille relative des chiens :")
    for taille in dogs_relatives_tailles:
        print(f"{taille:.2f}")
     #afficher_formes_oreilles(oreilles_chats, oreilles_chiens):
    print("Formes des oreilles des chats :")
    for img, forme in cats_ears_shapes.items():
        print(f"{img}: {forme}")
    
    print("\nFormes des oreilles des chiens :")
    for img, forme in dogs_ears_shapes.items():
        print(f"{img}: {forme}")

    # Afficher un message de confirmation
    messagebox.showinfo("Entraînement terminé", "Les données ont été extraites avec succès !")



#***** fonction pour choisir une nouvelle image 
def browse_image():
    path = filedialog.askopenfilename(
        title="Sélectionner une image",
        filetypes=[("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if path:
        img = Image.open(path)
        img = img.resize((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        return img_tk
# Appeler la fonction pour sélectionner une image
image_selectionne = browse_image()

def moyenne(liste):
    if len(liste) == 0:
        return 0
    return sum(liste) / len(liste)

def distance_simple(a, b):
    return abs(a - b)

def predir_animal(img_path):

    # Étape 1 : Extraire les caractéristiques de l'image cible
    color_dominant = extract_dominant_color(img_path)
    eyes_shape = detect_eye_shapes(img_path)
    relative_size = estimer_taille_animal(img_path)
    ears_shape = detect_ear_shape(img_path)

    # Remplacer None par 0 si besoin
    if eyes_shape is None:
        eyes_shape = 0
    if ears_shape is None:
        ears_shape = 0

    # Étape 2 : Moyennes de chaque classe
    moy_cat_color = moyenne(cats_colors)
    moy_dog_color = moyenne(dogs_colors)

    moy_cat_eyes = moyenne(cat_eye_shapes)
    moy_dog_eyes = moyenne(dog_eye_shapes)

    moy_cat_size = moyenne(cats_relatives_tailles )
    moy_dog_size = moyenne(dogs_relatives_tailles )

    moy_cat_ears = moyenne(cats_ears_shapes)
    moy_dog_ears = moyenne(dogs_ears_shapes)

    # Étape 3 : Calculer la "distance" à chaque classe
    dist_cat = (distance_simple(color_dominant, moy_cat_color) +
                distance_simple(eyes_shape, moy_cat_eyes) +
                distance_simple(relative_size, moy_cat_size) +
                distance_simple(ears_shape, moy_cat_ears))

    dist_dog = (distance_simple(color_dominant, moy_dog_color) +
                distance_simple(eyes_shape, moy_dog_eyes) +
                distance_simple(relative_size, moy_dog_size) +
                distance_simple(ears_shape, moy_dog_ears))

    # Étape 4 : Calculer le pourcentage de similarité
    total_distance = dist_cat + dist_dog
    if total_distance == 0:
        percent_cat = 50  # Dans ce cas, l'image est équidistante des deux classes.
        percent_dog = 50
    else:
        percent_cat = (dist_dog / total_distance) * 100
        percent_dog = (dist_cat / total_distance) * 100

    # Étape 5 : Choisir la classe la plus proche
    if dist_cat < dist_dog:
        prediction = "chat"
    elif dist_dog < dist_cat:
        prediction = "chien"
    else:
        prediction = "Inconnu"

    # Affichage des résultats avec pourcentage
    print(f"Image : {img_path}")
    print(f" - Couleur dominante : {color_dominant}")
    print(f" - Forme yeux : {eyes_shape}")
    print(f" - Taille relative : {relative_size:.2f}")
    print(f" - Oreilles détectées : {ears_shape}")
    print(f" - Distance Chat : {dist_cat:.2f}")
    print(f" - Distance Chien : {dist_dog:.2f}")
    print(f" - Prédiction : {prediction}")
    print(f" - Pourcentage Chat : {percent_cat:.2f}%")
    print(f" - Pourcentage Chien : {percent_dog:.2f}%")

    return prediction, percent_cat, percent_dog

"""
#************fonction faire prediction de l image que l utilisateurfait selectionner dans interface 2
def predict_image(img_path):
    total_score_cat = 0
    total_score_dog = 0
    dominant_color = extract_dominant_color(img_path)
    
    # shape of eyes
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    eye_shape = "inconnu"
    for (x, y, w, h) in eyes:
        ratio = w / h
        eye_shape = "rond" if ratio < 1.2 else "allongé"
        break

    # Comparaison des couleurs
    color_distance_cat = compare_color_distance(dominant_color, cats_colors)
    color_distance_dog = compare_color_distance(dominant_color, dogs_colors)

    # Comparaison des yeux
    eye_score_cat = 0 if eye_shape in cat_eye_shapes else 1
    eye_score_dog = 0 if eye_shape in dog_eye_shapes else 1

   
    # Forme des oreilles
    ear_shape = detect_ear_shape(img_path)

    # Extraire les formes d'oreilles des images d'entraînement
    cat_ears = [detect_ear_shape(os.path.join(CAT_FOLDER, f)) 
                for f in os.listdir(CAT_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    dog_ears = [detect_ear_shape(os.path.join(DOG_FOLDER, f)) 
                for f in os.listdir(DOG_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    matched_cat = cat_ears.count(ear_shape)
    matched_dog = dog_ears.count(ear_shape)

    ear_score_cat = matched_cat / len(cat_ears) if len(cat_ears) > 0 else 0
    ear_score_dog = matched_dog / len(dog_ears) if len(dog_ears) > 0 else 0
    # Calcul total des scores
    total_score_cat = color_distance_cat + (eye_score_cat * 50) + (1 - ear_score_cat) * 50
    total_score_dog = color_distance_dog + (eye_score_dog * 50) + (1 - ear_score_dog) * 50

    if total_score_cat < total_score_dog:
        confidence = max(50, int(100 - total_score_cat))
        return f"{confidence}% chat"
    else:
        confidence = max(50, int(100 - total_score_dog))
        return f"{confidence}% chien"
"""
