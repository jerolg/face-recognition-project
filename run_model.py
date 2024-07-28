import time
import os
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#import tflite_runtime.interpreter as tflite
import tensorflow as tf

class Watcher:
    DIRECTORY_TO_WATCH = "execution/array_images"
    OUTPUT_DIRECTORY = "execution/predictions"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.OUTPUT_DIRECTORY)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            self.process_file(event.src_path, self.output_directory)

    def process_file(self, file_path, output_directory):
        # Carga el array desde el archivo .npy
        try:
            image_array = np.load(file_path)
        except Exception as e:
            print(f"Error al cargar el archivo .npy: {e}")
            return

        # Carga el modelo TFLite y asigna los tensores
        interpreter = tf.lite.Interpreter(model_path="tflite-model/tflite-model-2/model (1).tflite")
        interpreter.allocate_tensors()

        # Obtiene los tensores de entrada y salida
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_data = np.array(image_array, dtype=np.float32)
        print(input_data.shape)
        if not np.array_equal(input_data.shape, input_details[0]['shape']):
            print(f"Forma de entrada incorrecta: se esperaba {input_details[0]['shape']} pero se obtuvo {input_data.shape}")
            return

        # Establece el tensor de entrada
        interpreter.set_tensor(input_details[0]['index'], input_data)
        print("Tensor de entreda cargado correctamente")

        # Invoca el intérprete
        interpreter.invoke()
        print("Interprete invocado")

        # Obtiene el resultado
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print(f"Prediction {output_data}")

        # Guarda el resultado en el directorio de salida
        output_file_path = os.path.join(output_directory, "out_" + os.path.basename(file_path))
        np.save(output_file_path, output_data)
        print(f"Resultado guardado en: {output_file_path}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
