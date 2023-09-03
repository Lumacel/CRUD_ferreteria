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
    """Reorganiza la lista para facilitar la busqueda de cada articulo
    """
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
                        row[9]= f"{float(row[9]):.2f}"
                    except ValueError:
                        continue
                    row[8] = row[8].upper()
                    row[8]= row[8].translate(row[8].maketrans('ÁÉÍÓÚÜ','AEIOUU'))

                    if row[1]== "100" and "ADHESIVO DE CONTACTO" not in row[8]:
                        row[8]= "ADHESIVO DE CONTACTO " + row[8]
                    if row[1]== "200" and "ADHESIVO EPOXI" not in row[8]:
                        row[8]= "ADHESIVO EPOXI " + row[8]
                    if row[1]== "200" and "BURL" not in row[8]:
                        row[8]= "BURLETE " + row[8]
                    if row[1]== "800"  and "PISTOLA" not in row[8]:
                        row[8]= "PISTOLA APLICADORA " + row[8]
                    if row[1]== "850"  and "PISTOLA" not in row[8]:
                        row[8]= "PISTOLA ENCOLADORA " + row[8]
                    if row[1]== "1300"  and "TOPETINA" not in row[8]:
                        row[8]= "TOPETINA " + row[8]
                    if row[1]== "1400"  and "ZOCALO" not in row[8]:
                        row[8]= "ZOCALO " + row[8]
                    if row[1]== "2500"  and "CANDADO" not in row[8]:
                        row[8]= "CANDADO " + row[8]
                    if row[1]== "2900":
                        row[8]= "DESTORNILLADOR " + row[8]
                    if row[1]== "3050" and "DISCO ABRASIVO" not in row[8]:
                        row[8]= "DISCO ABRASIVO DE CORTE " + row[8]
                    if row[1]== "3051" and "DISCO ABRASIVO" not in row[8]:
                        row[8]= "DISCO ABRASIVO DE DESBASTE " + row[8]
                    if row[1]== "3000" and "DISCO DIAMANTADO" not in row[8]:
                        row[8]= "DISCO DIAMANTADO " + row[8]
                    if row[1]== "3200"  and "ESPATULA" not in row[8]:
                        row[8]= "ESPATULA " + row[8]
                    if row[1]== "3605"  and "LIMA" not in row[8]:
                        row[8]= "LIMA SERIE 500 " + row[8]
                    if row[1]== "4150"  and "PINZA" not in row[8]:
                        row[8]= "PINZA " + row[8]
                    if row[1]== "4700"  and "SERRUCHO" not in row[8]:
                        row[8]= "SERRUCHO " + row[8]
                    if row[1]== "4300"  and "TIJERA" not in row[8]:
                        row[8]= "TIJERA " + row[8]

                    row= [row[0],f"{row[8]} -- {row[5]} ({row[2]})",row[9]]
                    row.append(distribuidora)

                    writer_object.writerow(row)

                    cont+=1
                    print(cont,row)

    except FileNotFoundError as error:
        print(error)
        return None

    return nombre_arch_csv.split("\\")[1]

if __name__== "__main__":
    DISTRIBUIDORA= "SUPRABOND"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
