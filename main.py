import numpy as np
import pandas as pd
import pandas as pd
import tkinter as tk
from tkinter import ttk
import pyperclip as pc
import re
import os
from tqdm import tqdm
from io import StringIO
import threading
import time


# Cambia el directorio de trabajo al directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Cargar el archivo JSON como un DataFrame
APUS_prueba = []
with open('data.json', 'r') as file:
    lines = file.readlines()
    for line in tqdm(lines, desc="Cargando Dataframe: "):
        # Cargar el diccionario de DataFrames desde el archivo JSON
        data = pd.read_json(StringIO(line.strip()), typ='series').to_dict()
        for key, value in data.items():
            # Reconstruir cada DataFrame con su nombre original
            idx = int(key.split('_')[1])  # Obtener el índice del DataFrame del nombre de la clave
            if len(APUS_prueba) <= idx:  # Asegurarse de que haya suficientes elementos en la lista
                APUS_prueba.extend([pd.DataFrame()] * (idx - len(APUS_prueba) + 1))
            APUS_prueba[idx] = pd.DataFrame(value)

# APU_completados ahora contiene la lista de DataFrames originales

def copy_tabla():
    if not tabla_data:
        result_text.set("Error: No hay datos para copiar.")
        return

    # Crear el DataFrame con los datos de la tabla
    columns_to_include_1 = ["ITEM - Descripción", "", "Unidad", "Cant", "Desper", "Vr/Unitario", "Vr/Parcial"]
    columns_to_include = ["ITEM - Descripción", "Unidad", "Cant", "Desper", "Vr/Unitario", "Vr/Parcial"]

    tabla_df = pd.DataFrame(tabla_data, columns=tabla_columns)
    tabla_df = tabla_df[columns_to_include]

    # Insertar una columna en blanco
    tabla_df.insert(1, '', '')


    # Unir los valores de las columnas 'Codigo', 'Descripcion', 'UnidadAPU' para la primera línea
    header = f"{tabla_data[0][-3]} {tabla_data[0][-2]} {tabla_data[0][-1]}\n"
    
    # Convertir el DataFrame en una cadena con encabezados de columnas en la segunda línea
    columns = "\t".join(columns_to_include_1) + "\n"

    # Convert the DataFrame to CSV string without index and header
    data_string = tabla_df.to_csv(index=False, header=False, sep='\t', lineterminator = '\r').strip()
    
    # Seleccionar los valores de la primera fila de las columnas especificadas
    valores_headers = ["Materiales", "Equipo", "AIU", "SubTotal", "Mano de Obra", "Otros", "VALOR TOTAL"]
    valores = tabla_data[0][-10:-3]  # Ajustar los índices según las posiciones correctas
    valores_string = "\t".join(map(str, valores)) + "\n"
    valores_headers_string = "\t".join(valores_headers) + "\n"

    # Combinar todos los componentes en una sola cadena
    final_string = header + columns + data_string + "\n" + valores_headers_string + valores_string
 
    # Copiar al portapapeles
    ventana.clipboard_clear()
    ventana.clipboard_append(final_string)
    ventana.update()  # Esto asegura que el portapapeles se actualice correctamente

    result_text.set("Dataframe copiado")


def buscar_apu():
    global tabla_data, tabla_columns
    codigo_busqueda = codigo_entry.get().upper()  # Obtener código y convertir a mayúsculas

    for df in APUS_prueba:
        if codigo_busqueda in df['Codigo'].values:
            # Limpiar resultados anteriores
            tabla_data = []
            tabla_columns = df.columns.tolist()

            # Insertar filas en la tabla
            for index, row in df.iterrows():
                values = [row[col] for col in df.columns]
                tabla_data.append(values)

            result_text.set("APU lista para copiar")
            return

    # Código no encontrado
    tabla_data = []
    result_text.set("Código no encontrado.")

def buscar_por_palabras_clave():
    palabra_clave = palabra_clave_entry.get().lower()
    coincidencias = []

    for df in APUS_prueba:
        if 'Descripcion' in df.columns:
            coincidencias.extend(df[df['Descripcion'].fillna('').str.lower().str.contains(palabra_clave)].to_dict('records'))

    mostrar_coincidencias(coincidencias)

def mostrar_coincidencias(coincidencias):
    coincidencias_listbox.delete(0, tk.END)

    if coincidencias:
        for coincidencia in coincidencias:
            coincidencias_listbox.insert(tk.END, f"{coincidencia['Codigo']} - {coincidencia['Descripcion']}")
    else:
        coincidencias_listbox.insert(tk.END, "No hay coincidencias")
        
def seleccionar_apu(event):
    seleccion = coincidencias_listbox.curselection()
    if seleccion:
        index = seleccion[0]
        if coincidencias_listbox.get(index) != "No hay coincidencias":
            codigo_seleccionado = coincidencias_listbox.get(index).split(" - ")[0]
            codigo_entry.delete(0, tk.END)
            codigo_entry.insert(0, codigo_seleccionado)
            buscar_apu()



def animacion_cargando():
    i = 1
    while cargando:
        result_text.set("Cargando " + ". " * i)
        ventana.update()
        time.sleep(0.2)
        i = (i % 3) + 1  # Cicla entre 1, 2 y 3

def buscar_con_animacion():
    global cargando
    cargando = True

    # Iniciar el hilo de animación
    hilo_animacion = threading.Thread(target=animacion_cargando)
    hilo_animacion.start()

    # Realizar la búsqueda en otro hilo
    hilo_busqueda = threading.Thread(target=buscar_por_palabras_clave_y_detener_animacion)
    hilo_busqueda.start()

def buscar_por_palabras_clave_y_detener_animacion():
    buscar_por_palabras_clave()

    # Detener la animación
    global cargando
    cargando = False
    result_text.set("Búsqueda completada")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Buscador de APUs")

codigo_label = ttk.Label(ventana, text="Código APU (XX-XX-XX):")
codigo_label.grid(row=0, column=0, padx=5, pady=5)

codigo_entry = ttk.Entry(ventana)
codigo_entry.grid(row=0, column=1, padx=5, pady=5)

buscar_button = ttk.Button(ventana, text="Buscar", command=buscar_apu)
buscar_button.grid(row=0, column=2, padx=5, pady=5)

# Campo para palabras clave
palabra_clave_label = ttk.Label(ventana, text="Palabras Clave:")
palabra_clave_label.grid(row=1, column=0, padx=5, pady=5)

palabra_clave_entry = ttk.Entry(ventana)
palabra_clave_entry.grid(row=1, column=1, padx=5, pady=5)

buscar_clave_button = ttk.Button(ventana, text="Buscar", command=buscar_con_animacion)
buscar_clave_button.grid(row=1, column=2, padx=5, pady=5)

# Lista de coincidencias
coincidencias_listbox = tk.Listbox(ventana, width=100, height=10)  # Ajustar el ancho y alto aquí
coincidencias_listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
coincidencias_listbox.bind("<<ListboxSelect>>", seleccionar_apu)

# Texto para mostrar resultados
result_text = tk.StringVar()
result_label = ttk.Label(ventana, textvariable=result_text, wraplength=300)
result_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Botón para copiar al portapapeles
copy_button = ttk.Button(ventana, text="Copiar al Portapapeles", command=copy_tabla)
copy_button.grid(row=4, column=2, padx=5, pady=5)

tabla_data = []
tabla_columns = []

cargando = False

ventana.mainloop()