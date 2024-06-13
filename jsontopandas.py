import numpy as np
import pandas as pd

# Cargar el archivo JSON y reconstruir la lista de DataFrames originales
APUS_prueba = []
with open('data.json', 'r') as file:
    for line in file:
        # Cargar el diccionario de DataFrames desde el archivo JSON
        data = pd.read_json(line.strip(), typ='series').to_dict()
        for key, value in data.items():
            # Reconstruir cada DataFrame con su nombre original
            idx = int(key.split('_')[1])  # Obtener el índice del DataFrame del nombre de la clave
            if len(APUS_prueba) <= idx:  # Asegurarse de que haya suficientes elementos en la lista
                APUS_prueba.extend([pd.DataFrame()] * (idx - len(APUS_prueba) + 1))
            APUS_prueba[idx] = pd.DataFrame(value)

# APU_completados ahora contiene la lista de DataFrames originales

#print(APUS_prueba[40])