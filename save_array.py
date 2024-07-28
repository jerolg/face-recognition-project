import cv2
import numpy as np
import os

def process_and_save_image(image_file, output_file):
    # Inicializar array para la imagen
    image_array = []

    # Leer y procesar la imagen
    try:
        img = cv2.imread(image_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (96, 96))
        image_array.append(img)
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")

    # Normalizar y guardar la imagen
    if image_array:
        image_array = np.array(image_array) / 255.0
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Crear el directorio si no existe
        np.save(output_file, image_array)
        print(f"Imagen procesada y guardada en: {output_file}")
    else:
        print("No se pudo procesar la imagen.")

image_file = "execution/images/20221129_173820_293 (1).jpg"
output_dir = "execution/array_images"
output_base = os.path.basename(image_file)
output_file = os.path.join(output_dir, os.path.splitext(output_base)[0] + ".npy")

print(output_file)
process_and_save_image(image_file, output_file)

