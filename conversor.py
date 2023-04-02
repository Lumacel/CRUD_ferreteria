import pandas as pd
from tkinter import filedialog
import os

def convertir_a_csv():  # separa hojas de documentos Excel (.xls y .xlsx) y los convierte a formato .csv
    archivo = filedialog.askopenfilename(filetypes =[('Excel Files', '*.xlsx'),('Excel Files', '*.xls')])
    if archivo== "":
        return []
    else:
        name = os.path.basename(archivo)
        path = os.path.dirname(archivo)
        archivo_excel = pd.ExcelFile(archivo)
        nombres_hojas = archivo_excel.sheet_names

        if name.endswith(".xls"):
            for i in nombres_hojas:
                print(i)
                df = pd.read_excel(archivo, sheet_name=i)
                if df.empty: continue
                if df.shape[1]< 3: continue  # cantidad de columnas
                
                df.to_csv(f'{path}/{i}.csv', index=False, encoding='utf-8-sig')
        elif name.endswith(".xlsx"):
            for i in nombres_hojas:
                print(i)
                df = pd.read_excel(archivo, sheet_name=i, engine='openpyxl')
                if df.empty: continue
                if df.shape[1]< 3: continue  # cantidad de columnas

                df.to_csv(f'{path}/{i}.csv', index=False, encoding='utf-8-sig')
        else: pass

        lista_nueva_arch = []
        lista_arch_bn = os.listdir(path)

        for arch in lista_arch_bn:
            if arch.endswith(".csv"):
                lista_nueva_arch.append(f"{path}//{arch}")
            else: continue
            
        return lista_nueva_arch


if __name__== "__main__":
    lista_nueva_arch = convertir_a_csv()
    print(lista_nueva_arch)

