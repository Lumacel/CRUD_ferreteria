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
    if "Hoja2" in file:
        pass  # filtra hoja2
    else:
        items= {0: 'Ruberoi', 1: 'Telgopor ( Dólar oficial)', 2: 'Membranas',
                3: 'MEMBRANA EN PASTA',4: 'MEMBRANA EN PASTA FIBRADA',5: 'VENDA DE TELA',
                6: 'LATEX PREMIUM',7: 'LATEX LINEA DECOR',8: 'ENDUIDO PLASTICO',
                9: 'REVESTIMIENTO PLASTICO',10: 'Pintura Asfaltica',11: 'Espumas para techo.',
                12: 'Hormigoneras Economica', 13: ',Hormigoneras SuperReforzada',14: 'Carretillas',
                15: 'Repuestos para hormigonera',16: 'Ruedas', 17: 'Carritos de Carga',
                18: 'Precio Por Escalon', 19: 'Escalon Familiar',20: 'Escalon Pintor de 4 a 10',
                21:'Escalon Pintor de 11 a 12', 22: 'Escaleras',23: 'Articulos de Pino',
                24: 'Herramientas de Albaliñeria', 25: 'Fieltros de Espuma',
                26: 'Calefones', 27: 'Clavos y Alambre'}
        # veriables para calcular precio de las escaleras segun cantidad de escalones
        txt_ini = ""
        txt_fin = ""
        cant_famil= 3
        cant_pint=4
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
                                row = [item.strip(" $") for item in row]
                                row.remove('')
                        except ValueError:
                            pass

                        if row == [] or  len(row)>2 : continue
                        if len(row)==1 and not row[0] in items.values():
                            continue
                        if  items[0] in row[0]:
                            txt_ini ="RUBEROI "
                            continue
                        if items[1] in row[0]:
                            txt_ini =""
                            continue
                        if items[2] in row[0]:
                            txt_ini ="MEMB "
                            continue
                        if items[3] in row[0] or items[4] in row[0]:
                            txt_ini =""
                            continue
                        if items[5] in row[0]:
                            continue
                        if items[6] in row[0]:
                            txt_fin =" (PREMIUM)"
                            continue
                        if items[7] in row[0]:
                            txt_fin =" (DECOR)"
                            continue
                        if items[8] in row[0]:
                            txt_fin =""
                            continue
                        if items[9] in row[0]:
                            continue
                        if items[10] in row[0]:
                            continue
                        if items[11] in row[0]:
                            continue
                        if items[12] in row[0]:
                            continue
                        if items[13] in row[0]:
                            txt_fin =" (SUPER-REFORZADA)"
                            continue
                        if items[14] in row[0]:
                            txt_fin =""
                            continue
                        if items[15] in row[0]:
                            txt_fin =" (REPUESTO HORMIGONERA)"
                            continue
                        if items[16] in row[0]:
                            txt_ini ="Rueda "
                            txt_fin = ""
                            continue
                        if items[17] in row[0]:
                            txt_ini =""
                            continue
                        if items[18] in row[0]:
                            continue
                        if items[19] in row[0]:
                            prec_famil= row[1] # precio Escalon Familiar de 4 a 10
                            continue
                        if items[20] in row[0]:
                            prec_pint_4_10= row[1] # precio Escalon Pintor de 4 a 10
                            continue
                        if items[21] in row[0]:
                            prec_pint_11_12= row[1] # precio Escalon Pintor de 11 a 12
                            continue
                        if items[22] in row[0]:
                            continue
                        if items[23] in row[0]:
                            txt_fin = " (Artic. de pino)"
                            txt_ini= ""
                            continue
                        if items[24] in row[0]:
                            txt_ini= ""
                            txt_fin = ""
                            continue
                        if items[25] in row[0]:
                            continue
                        if items[26] in row[0]:
                            txt_ini = "Calefon "
                            continue
                        if items[27] in row[0]:
                            continue
                        if row[0].startswith("Familiar"):
                            txt_ini= "Escalera "
                            row[0] = f"{row[0]} ({row[1]})"
                            row[1] = str(float(prec_famil)*cant_famil)
                            cant_famil+=1
                        if row[0].startswith("Pintor"):
                            row[0] = f"{row[0]} ({row[1]})"
                            row[1] = str(float(prec_pint_4_10 if cant_pint <11 else prec_pint_11_12)*cant_pint)
                            cant_pint+=1

                        row= ["S/CODIGO",
                               txt_ini+row[0]+txt_fin if txt_ini not in row[0] else row[0]+txt_fin,
                                 row[1]]

                        row[1]= row[1].upper()
                        row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
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
    return None

if __name__== "__main__":
    DISTRIBUIDORA= "LOS_PINOS"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
        