"""Este modulo crea un archivo .csv con la informacion que hay en
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
    """Reorganiza la lista para facilitar la busqueda de cada articulo"""
    cont= 0  
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename
    try:
        with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
            writer_object = csv.writer(new_csvfile)
            with open(file, "r", encoding= 'utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    comienzo=""
                    try:
                        while True:
                            row.remove('')
                    except ValueError:
                        pass
                    if row == []: continue
                    if row[0].startswith("    "): continue
                    try:
                        row= [row[1],row[0],row[3]]
                    except Exception:
                        continue
                    row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ±Ð','AEIOUUÑÑ'))
                    row[1]= row[1].upper().rstrip()
                    if row[1].startswith("TOMA ") or row[1].startswith("MULTIPLE") or row[1].startswith("MEGA BIN") or row[1].startswith("BASE BINO"): 
                        comienzo = "ZAPATILLA " 
                    else:
                        comienzo = ""
                
                    row[1]= comienzo + row[1]
                    try:
                        row[2]= float(row[2])*.56 # coeficiente DANIROX = .56 (precio lista -30% - 20%)
                        row[2]= f"{(row[2]):.2f}"
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
    DISTRIBUIDORA= "DANIROX"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, DISTRIBUIDORA)
        