import csv
import os
from datetime import datetime 
from tkinter import filedialog

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    if "Hoja2" in file: pass  # filtra hoja2
    else:                      
        items= {0: 'Ruberoi', 1: 'Telgopor ( Dólar oficial)', 2: 'Membranas', 3: 'MEMBRANA EN PASTA', 4: 'MEMBRANA EN PASTA FIBRADA', 
                5: 'VENDA DE TELA', 6: 'LATEX PREMIUM', 7: 'LATEX LINEA DECOR', 8: 'ENDUIDO PLASTICO', 9: 'REVESTIMIENTO PLASTICO', 
                10: 'Pintura Asfaltica', 11: 'Espumas para techo.', 12: 'Hormigoneras Economica', 13: ',Hormigoneras SuperReforzada', 
                14: 'Carretillas', 15: 'Repuestos para hormigonera', 16: 'Ruedas', 17: 'Carritos de Carga', 18: 'Precio Por Escalon', 
                19: 'Escalon Familiar', 20: 'Escalon Pintor de 4 a 10', 21:'Escalon Pintor de 11 a 12', 22: 'Escaleras', 
                23: 'Articulos de Pino', 24: 'Herramientas de Albaliñeria', 25: 'Fieltros de Espuma', 26: 'Calefones', 27: 'Clavos y Alambre'}
        texto_inicial = ""
        texto_final = ""
        cant_familiar= 3
        cant_pintor=4

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
                            while True:
                                for a in range(len(row)):
                                    row[a] = row[a].strip(" $")
                                row.remove('')
                        except ValueError:
                            pass

                        if row == [] or  len(row)>2 : continue
                        if len(row)==1 and not row[0] in items.values(): continue

                        if  items[0] in row[0]: 
                            texto_inicial ="RUBEROI "
                            continue
                        elif items[1] in row[0]:
                            texto_inicial =""
                            continue
                        elif items[2] in row[0]: 
                            texto_inicial ="MEMB "
                            continue
                        elif items[3] in row[0] or items[4] in row[0]:
                            texto_inicial =""
                            continue
                        elif items[5] in row[0]: continue
                        elif items[6] in row[0]: 
                            texto_final =" (PREMIUM)"
                            continue
                        elif items[7] in row[0]:
                            texto_final =" (DECOR)"
                            continue
                        elif items[8] in row[0]:
                            texto_final =""
                            continue
                        elif items[9] in row[0]: continue
                        elif items[10] in row[0]: continue
                        elif items[11] in row[0]: continue
                        elif items[12] in row[0]: continue
                        elif items[13] in row[0]: 
                            texto_final =" (SUPER-REFORZADA)"
                            continue
                        elif items[14] in row[0]: 
                            texto_final =""
                            continue
                        elif items[15] in row[0]:
                            texto_final =" (REPUESTO HORMIGONERA)"
                            continue
                        elif items[16] in row[0]:
                            texto_inicial ="Rueda "
                            texto_final = ""
                            continue
                        elif items[17] in row[0]:
                            texto_inicial =""
                            continue
                        elif items[18] in row[0]:
                            continue
                        elif items[19] in row[0]:
                            precio_familiar= row[1] # precio Escalon Familiar de 4 a 10
                            continue
                        elif items[20] in row[0]:
                            precio_pintor_4_10= row[1] # precio Escalon Pintor de 4 a 10
                            continue
                        elif items[21] in row[0]:
                            precio_pintor_11_12= row[1] # precio Escalon Pintor de 11 a 12
                            continue
                        elif items[22] in row[0]: continue
                        elif items[23] in row[0]: 
                            texto_final = " (Artic. de pino)"
                            texto_inicial= ""
                            continue
                        elif items[24] in row[0]: 
                            texto_inicial= ""
                            texto_final = ""
                            continue
                        elif items[25] in row[0]: continue
                        elif items[26] in row[0]: 
                            texto_inicial = "Calefon "
                            continue
                        elif items[27] in row[0]: continue
                        elif row[0].startswith("Familiar"):
                            texto_inicial= "Escalera "
                            row[0] = f"{row[0]} ({row[1]})"
                            row[1] = str(float(precio_familiar)*cant_familiar)
                            cant_familiar+=1
                        elif row[0].startswith("Pintor"):
                            row[0] = f"{row[0]} ({row[1]})"
                            row[1] = str(float(precio_pintor_4_10 if cant_pintor <11 else precio_pintor_11_12)*cant_pintor)
                            cant_pintor+=1
                                        
                        row= ["S/CODIGO", texto_inicial + row[0] + texto_final if texto_inicial not in row[0] else row[0] + texto_final, row[1]] 

                        row[1]= row[1].upper()
                        row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                        try:
                            row[2]= f"{float(row[2]):.2f}"
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
    distribuidora = "LOS_PINOS"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, distribuidora)
        