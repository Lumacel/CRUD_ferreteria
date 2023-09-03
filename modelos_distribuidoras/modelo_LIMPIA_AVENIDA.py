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
    if "CAMBIOS" in file: ###### filtra hoja que tiene informacion sobre los cambios
        pass
    else:
        cont=0
        basename = os.path.basename(file)
        nombre_arch_csv= nombrar_archivo(distribuidora) + basename
        try:
            with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
                writer_object= csv.writer(new_csvfile)
                with open(file, "r", encoding='utf-8-sig') as csvfile:
                    spamreader= csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        try:
                            while True:
                                row.remove('')
                        except ValueError:
                            pass
                        if row == []:
                            continue
                        if len(row)<3:
                            continue
                        row[1] = row[1].rstrip(" ").upper()
                        row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                        try:
                            row[2]= f"{float(row[2]):.2f}"
                        except ValueError:
                            continue
                        match row[0][0:7]:
                            case "A-24035"|"A-24036"|"A-24037":
                                row[1]= "ALICATE CORTE OBLICUO " + row[1] + " (METZ)"
                            case "P-06911"|"P-06912":
                                row[1]= "PINZA MEDIA CAÑA AISLADA " + row[1] + " (METZ)"
                            case "P-06914"|"P-06915":
                                row[1]= "PINZA PUNTA CHATA " + row[1] + " (METZ)"
                            case "P-06911"|"P-06912":
                                row[1]= "PINZA MEDIA CAÑA AISLADA " + row[1] + " (METZ)"
                            case "P-06914"|"P-06915":
                                row[1]= "PINZA PUNTA CHATA " + row[1] + " (METZ)"
                            case "P-06918":
                                row[1]= "PINZA PUNTA CURVA " + row[1] + " (METZ)"
                            case "P-06941"|"P-06942":
                                row[1]= "PINZA ROSARIO PARA ARTESANIA " + row[1] + " (METZ)"
                            case "P-06914"|"P-06915":
                                row[1]= "PINZA PUNTA CHATA " + row[1] + " (METZ)"

                        match row[0][0:6]:
                            case "C-1427"|"C-1428":
                                row[1]= row[1] + " (DESTAPACIONES) "
                            case "T-0391":
                                row[1]= "TENAZA PARA CARPINTEROS AISLADAS " + row[1] + " (METZ)"
                            case "T-0380":
                                row[1]= "TENAZA PARA ARMADORES AISLADAS " + row[1] + " (METZ)"
                            case "P-0697":
                                row[1]= "PINZA UNIVERSAL AISLADA " + row[1] + " (METZ)"
                            case "E-0106":
                                row[1]= "ESCALERA METALICA " + row[1]
                            case "S-0445"|"S-0446"|"S-0447":
                                row[1]= "SOGA MULTIFILAMENTO. PROLIPROP " + row[1]
                            case "P-0172":
                                row[1]= "PAPEL DE LIJA " + row[1]
                            case "T-0350":
                                row[1]= "TELA DE ESMERIL " + row[1]
                            case "A-0149"|"A-0150"|"A-0151"|"A-0152"|"A-0153":
                                row[1]= "GRASA POTE " + row[1]
                            case  "A-0145"|"A-0146"|"A-0147"|"A-0148"|"A-0154"|"A-0155":
                                row[1]= "LUBRICANTE " + row[1]
                            case "A-0138"|"A-0139":
                                row[1]= "ACEITERA CON BOMBA " + row[1]
                            case "B3001"|"B-3002":
                                row[1]= "BISAGRA HIERRO BRONCEADO (CHINA) " + row[1] + " (REHIN)"
                            case "B-2999"|"B-3000":
                                row[1]= "BISAGRA HIERRO PULIDO (CHINA) " + row[1] + " (REHIN)"
                            case "S-0350"|"S-0351":
                                row[1]= "SIERRA COPA BROCA ACERO TUNGSTENO " + row[1]
                            case "D-2308"|"D_2309":
                                row[1]= "DISCO YARD DHD " + row[1]
                            case "P-0672":
                                row[1]= "PINCEL " + row[1] + " (ESSAMET)"
                            case "L-3062":
                                row[1]= "LLAVE AJUSTABLE FOSFATIZADA " + row[1] + " (METZ)"
                            case "P-0692":
                                row[1]= "PINZA PICO DE LORO CON AISLACION " + row[1] + " (METZ)"

                        match row[0][0:5]:
                            case "A-001"|"A-002"|"A-003"|"A-007":
                                row[1]= "ABRAZADERA " + row[1]
                            case "E-039":
                                row[1]= "ESQUINERO PLANO CROMATIZADO " + row[1]
                            case "M-060"|"M-061"|"M-062"|"M-063"|"M-069"|"M-071":
                                row[1]= "MECHA CILINDRICA " + row[1]
                            case "T-014":
                                row[1]= "TANZA DE NYLON " + row[1]
                            case "L-304"|"L-305":
                                row[1]= "LLAVES HEXAGONALES TIPO ALLEN " + row[1]
                            case "D-037":
                                row[1]= "DESTORNILLADOR " + row[1] + " (METZ)"
                            case "M-077":
                                row[1]= "MENSULA DE HIERRO " + row[1] + " (CORVEX)"
                            case "B-305":
                                row[1]= "BISAGRAS PORTONES TIPO 'T' PROCEDENCIA CHINA" + row[1]
                            case "T-048":
                                row[1]= "TENSOR PARA SOGAS Y TOLDOS GALVANIZADOS " + row[1]
                        row.append(distribuidora)

                        writer_object.writerow(row)
                        cont+=1
                        print(cont,row)

        except FileNotFoundError as error:
            print(error)
            return None

        return nombre_arch_csv.split("\\")[1]
    return None


if __name__=="__main__":
    DISTRIBUIDORA= "LIMPIA_AVENIDA"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
        