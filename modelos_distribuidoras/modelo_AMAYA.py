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
                    row= [row[0],row[1],row[3]]
                    row[1] = row[1].upper()
                    row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                    row[1]=row[1].rstrip()
                    try:
                        row[2]= float(row[2])*.558 # .558 coeficiente AMAYA (precio lista -38% -10%)
                        row[2]= f"{(row[2]):.2f}"
                    except Exception:
                        continue
                    row.append(distribuidora)

                    writer_object.writerow(row)
                    c+=1
                    print(c,row)  
    except Exception as e:
        print(e)

    return nombre_arch_csv.split("\\")[1]

if __name__== "__main__":
    distribuidora = "AMAYA"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, distribuidora)
        