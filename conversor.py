"""Arma un archivo csv con cada  hoja del documento Excel (.xls y .xlsx)"""

import os
from tkinter import filedialog
import pandas as pd

def convertir_a_csv():
    """Separa hojas de documentos Excel (.xls y .xlsx) y 
    los convierte a formato .csv  
    """
    archivo = filedialog.askopenfilename(
        filetypes=[('Excel Files', '*.xlsx'), ('Excel Files', '*.xls')])
    print(archivo)
    if archivo == "":
        return []

    #name = os.path.basename(archivo)
    path = os.path.dirname(archivo)

    archivo_excel = pd.ExcelFile(archivo)
    nombres_hojas = archivo_excel.sheet_names

    lista_archivos_csv= []

    for hoja in nombres_hojas:
        print(hoja)
        dataframe = pd.read_excel(archivo, sheet_name= hoja)
        if dataframe.empty:
            continue
        if dataframe.shape[1] < 3: # cantidad de columnas
            continue

        nombre_archivo_csv = f"{path}/{hoja}.csv"

        dataframe.to_csv(nombre_archivo_csv, index=False, encoding='utf-8-sig')

        lista_archivos_csv.append(nombre_archivo_csv)

    return lista_archivos_csv

if __name__ == "__main__":
    lista_nueva = convertir_a_csv()
    print(lista_nueva)