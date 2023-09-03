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
    if "Hoja 1" in file:  ##### FILTRA LA HOJA 1 PORQUE TIENE LA MISMA INFORMACION QUE LA HOJA 2
        pass
    else:
        pinceles= ["LINEA","BLUE"]
        rodillos = ["LANA","SIMIL","ESPUMA","FORRADOS",
                    "EPOXI","ANTIGOTA","CUBREMAS","UNIVERSAL",
                    "ARTE FOAM", "LINEA HOGAR"]
        pinturas= ["SINT","LATEX","TEK","DURACRIL","MAMBA"]
        kuwait_claves= ["RODILLO","SILICONA","INFLANEUM","BARNIZ"]

        cont= 0
        basename = os.path.basename(file)
        nombre_arch_csv= nombrar_archivo(distribuidora) + basename
        try:
            with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
                writer_object = csv.writer(new_csvfile)
                with open(file, "r", encoding='utf-8-sig') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        row = [row[0], row[1]+ f" ({row[2]})", row[3]]
                        row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU')).upper()
                        row[1]=row[1].rstrip()
                        for i in pinceles:
                            if i in row[1]:
                                row[1]= "PINCEL " + row[1]
                        for i in rodillos:
                            if i in row[1]:
                                if "LLANA" in row[1]: continue
                                row[1]= "RODILLO " + row[1]
                        for i in pinturas:
                            if i in row[1]:
                                if i =="KUWAIT":
                                    for clave in kuwait_claves:
                                        if clave in row[1]: continue
                                if "PINTURA" in row[1]: continue
                                row[1] = "PINTURA " + row[1]
                        try:
                            row[2]= f"{float(row[2]):.2f}"
                        except ValueError:
                            continue
                        row.append(distribuidora)

                        writer_object.writerow(row)
                        cont+=1
                        print(cont, row)

        except FileNotFoundError as error:
            print(error)
            return None

        return nombre_arch_csv.split("\\")[1]

if __name__== "__main__":
    DISTRIBUIDORA= "ACF"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        if archivo.endswith("Hoja 1.csv"): continue # ignora primer hoja de dist. ACF
        normalizar_lista(archivo, DISTRIBUIDORA)

    