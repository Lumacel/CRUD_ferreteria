"""Este modulo arma un archivo .csv con la informacion que hay en
archivo original pero normaliza la cantidad de columnas y
corrige omisiones que pueden hacer dificil la busqueda de un articulo
"""
import csv
import os
from datetime import datetime 
from tkinter import filedialog

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    """Agrega encabezado al nombre del archivo con la fecha y hora actual
    """
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    cont= 0
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename
    try:
        with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
            writer_object = csv.writer(new_csvfile)
            with open(file, "r", encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    try:
                        while True:
                            row.remove('')
                    except ValueError:
                        pass
                    try:
                        if not row[0].isnumeric(): continue
                    except Exception:
                        continue
                    row[1] = row[1].upper()
                    row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                    row[1]=row[1].rstrip()
                    try:
                        row[2]= f"{float(row[2]):.2f}"
                    except ValueError:
                        continue
                    row.append(distribuidora)

                    writer_object.writerow(row)
                    cont+=1
                    print(cont,row)  
    except FileNotFoundError as error:
        print(error)
        return None
    
    return nombre_arch_csv.split("\\")[1]

if __name__== "__main__":
    DISTRIBUIDORA = "ARGENTINA"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
       
       


    