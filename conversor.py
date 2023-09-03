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
        archivo_excel = pd.ExcelFile(archivo)
        nombres_hojas = archivo_excel.sheet_names
        for i in nombres_hojas:
            print(i)
            dataframe = pd.read_excel(archivo, sheet_name=i)
            if dataframe.empty:
                continue
            if dataframe.shape[1] < 3:
                continue  # cantidad de columnas

            dataframe.to_csv(f'{path}/{i}.csv', index=False, encoding='utf-8-sig')

    elif name.endswith(".xlsx"):
        archivo_excel = pd.ExcelFile(archivo)
        nombres_hojas = archivo_excel.sheet_names
        for i in nombres_hojas:
            print(i)
            dataframe = pd.read_excel(archivo, sheet_name=i, engine='openpyxl')
            if dataframe.empty:
                continue
            if dataframe.shape[1] < 3:
                continue  # cantidad de columnas

            dataframe.to_csv(f'{path}/{i}.csv', index=False, encoding='utf-8-sig')

    else:
        pass

    lista_nueva_arch = []
    lista_arch_bn = os.listdir(path)

    for arch in lista_arch_bn:
        if arch.endswith(".csv"):
            lista_nueva_arch.append(f"{path}//{arch}")
        else:
            continue

    return lista_nueva_arch


if __name__ == "__main__":
    lista_nueva = convertir_a_csv()
    print(lista_nueva)
