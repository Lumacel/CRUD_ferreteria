import csv
import os
from datetime import datetime 
from tkinter import filedialog

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    c=0
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename
    try:
        with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
            writer_object = csv.writer(new_csvfile)
            with open(file, "r", encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    for i in range(2): row.remove(row[0]) 
                    try:
                        if row[1].startswith("LISTA") or row[0].startswith("CODIGO") :continue
                        row[1]= row[1].strip(" ").upper()
                        row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                        row[1]=row[1].rstrip()
                        try:
                            row[2]= f"{float(row[2]):.2f}"
                        except ValueError:
                            continue
                        row.append(distribuidora)
                        
                        writer_object.writerow(row)
                        c+=1
                        print(c,row)
                        
                    except Exception:
                        continue
    except Exception as e:
            print(e)
    return c

if __name__=="__main__":
    distribuidora = "LA_PLATA_LED"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, distribuidora)
        