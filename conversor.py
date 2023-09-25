"""Arma un archivo csv con cada  hoja del documento Excel (.xls y .xlsx)
"""
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

    name = os.path.basename(archivo)
    path = os.path.dirname(archivo)

    if name.endswith(".xls"):
        engine = 'xlrd' # archivos excel formato antiguo
    else:
        engine = 'openpyxl' # archivos excel formato nuevo

    archivo_excel = pd.ExcelFile(archivo)
    nombres_hojas = archivo_excel.sheet_names
    for hoja in nombres_hojas:
        print(hoja)
        dataframe = pd.read_excel(archivo, sheet_name= hoja, engine= engine )
        if dataframe.empty:
            continue
        if dataframe.shape[1] < 3: # cantidad de columnas
            continue

        dataframe.to_csv(f'{path}/{hoja}.csv', index=False, encoding='utf-8-sig')

    lista_nueva_archivos = []
    lista_achivos = os.listdir(path)

    for arch in lista_achivos:
        if arch.endswith(".csv"):
            lista_nueva_archivos.append(f"{path}//{arch}")
        else:
            continue

    return lista_nueva_archivos

if __name__ == "__main__":
    lista_nueva = convertir_a_csv()
    print(lista_nueva)
