import csv
import os
from datetime import datetime 
from tkinter import filedialog

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    c= 0
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
                    except Exception:
                        continue
                    row[8] = row[8].upper()
                    row[8]= row[8].translate(row[8].maketrans('ÁÉÍÓÚÜ','AEIOUU'))

                    if row[1]== "100" and "ADHESIVO DE CONTACTO" not in row[8]:
                        row[8]= "ADHESIVO DE CONTACTO " + row[8]
                        row[8]= "BURLETE " + row[8]
                    if row[1]== "200" and "ADHESIVO EPOXI" not in row[8]:
                        row[8]= "ADHESIVO EPOXI " + row[8]
                    if row[1]== "200" and "BURL" not in row[8]:
                        row[8]= "BURLETE " + row[8]
                    if row[1]== "800"  and "PISTOLA" not in row[8]:
                        row[8]= "PISTOLA APLICADORA " + row[8]
                    if row[1]== "850"  and "PISTOLA" not in row[8]:
                        row[8]= "PISTOLA ENCOLADORA " + row[8]
                    if row[1]== "1300"  and "TOPETINA " not in row[8]:
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

                    row= [row[0],f"{row[8]} -- {row[4]} {row[5]} ({row[2]})",row[9]]
                    row.append(distribuidora)

                    writer_object.writerow(row)
                   
                    c+=1
                    print(c,row)  
                    
    except Exception as e:
        print(e)

    return c #cantidad de items 

if __name__== "__main__":
    distribuidora = "SUPRABOND"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, distribuidora)
        