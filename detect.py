from ultralytics import YOLO
from PIL import Image
import torch
import os
import uuid

# Load model sekali
model = YOLO("best.pt")  # Sesuaikan dengan nama model kamu

def classify_leaf(image_path):
    # Prediksi dengan menyimpan gambar hasil deteksi
    results = model.predict(image_path, conf=0.5, save=True, project="results", name="detect", exist_ok=True)

    classes = model.names

    # Ambil label dari prediksi pertama
    if results and results[0].boxes:
        cls_id = int(results[0].boxes.cls[0].item())
        label = classes[cls_id]
    else:
        label = "tidak terdeteksi"

    # Ambil path gambar hasil deteksi
    detected_path = os.path.join(results[0].save_dir, os.path.basename(image_path))

    return label, detected_path
