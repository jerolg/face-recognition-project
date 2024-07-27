import os
import random
import shutil

def seleccionar_fotografias(dataset_path, destino_path, num_fotografias=100):
    # Obtener una lista de todas las subcarpetas en la carpeta principal
    subcarpetas = [os.path.join(dataset_path, subcarpeta) for subcarpeta in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, subcarpeta))]
    
    # Obtener una lista de todas las fotografías en todas las subcarpetas
    todas_fotografias = []
    for subcarpeta in subcarpetas:
        for archivo in os.listdir(subcarpeta):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                todas_fotografias.append(os.path.join(subcarpeta, archivo))
    
    # Seleccionar aleatoriamente 100 fotografías
    fotografias_seleccionadas = random.sample(todas_fotografias, num_fotografias)
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(destino_path):
        os.makedirs(destino_path)
    
    # Copiar las fotografías seleccionadas a la carpeta de destino
    for fotografia in fotografias_seleccionadas:
        shutil.copy(fotografia, destino_path)

# Ejemplo de uso
dataset_path = '/Users/aleja/Desktop/INSTRUMENTACION/dataset copy'
destino_path = '/Users/aleja/Desktop/INSTRUMENTACION/NoIdentificado'
seleccionar_fotografias(dataset_path, destino_path)
