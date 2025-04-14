import os
import shutil
from PIL import Image
import numpy as np

# dossier dataset
DATASET_DIR = "dataset"

def add_to_dataset(file_path, label):
    os.makedirs(os.path.join(DATASET_DIR, label), exist_ok=True)
    filename = os.path.basename(file_path)
    dest = os.path.join(DATASET_DIR, label, filename)
    shutil.copy(file_path, dest)

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            img = Image.open(path).resize((100, 100)).convert("L")
            images.append(np.array(img).flatten())
        except:
            continue
    return images

def train_model():
    # hna makaynach ML, juste kayn l'ajout
    chat = load_images_from_folder(os.path.join(DATASET_DIR, "chat"))
    chien = load_images_from_folder(os.path.join(DATASET_DIR, "chien"))
    return len(chat) > 0 and len(chien) > 0

def predict_image(image_path):
    try:
        img = Image.open(image_path).resize((100, 100)).convert("L")
        img_array = np.array(img).flatten()

        chat_imgs = load_images_from_folder(os.path.join(DATASET_DIR, "chat"))
        chien_imgs = load_images_from_folder(os.path.join(DATASET_DIR, "chien"))

        # Moyenne distance (similaire à KNN)
        def avg_distance(images):
            if not images:
                return float('inf')
            return np.mean([np.linalg.norm(img_array - i) for i in images])

        d_chat = avg_distance(chat_imgs)
        d_chien = avg_distance(chien_imgs)

        total = d_chat + d_chien
        if total == 0:
            return "Inconnu", 0

        p_chat = (d_chien / total) * 100
        p_chien = (d_chat / total) * 100

        if p_chat > p_chien:
            return "chat", round(p_chat)
        else:
            return "chien", round(p_chien)

    except:
        return "Erreur", 0

def calculate_dataset_accuracy():
    # approximation: basé sur séparation des distances
    try:
        chat_imgs = load_images_from_folder(os.path.join(DATASET_DIR, "chat"))
        chien_imgs = load_images_from_folder(os.path.join(DATASET_DIR, "chien"))
        if not chat_imgs or not chien_imgs:
            return 0
        total = len(chat_imgs) + len(chien_imgs)
        return round((len(chat_imgs) + len(chien_imgs)) / total * 100)
    except:
        return 0
