"""Este modulo crea un archivo .csv con la informacion que hay en
archivo original pero normaliza la cantidad de columnas y
corrige omisiones que pueden hacer dificil la busqueda de un articulo
"""
import os
from datetime import datetime
from tkinter import filedialog
import pandas as pd

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    """Agrega encabezado al nombre del archivo con la fecha y hora actual
    """
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    """Reorganiza la lista para facilitar la busqueda de cada articulo
    """
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file)

    try:
        columnas= {lista.columns[0] : 'codigo',
                    lista.columns[2] : 'detalle',
                    lista.columns[3] : 'precio'
                    }
        lista = lista.rename(columns= columnas)
        lista = lista[columnas.values()] # seleccionamos columnas que formaran dataframe
        lista = lista.dropna()
        lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
        lista['detalle'] = lista['detalle'].str.upper()
        lista['precio'] = lista['precio'].round(2)
        lista['distribuidora'] = distribuidora

        mapeo = {('SBD', 'ADHESIVO') : 'ADHESIVO DE CONTACTO ',
                ('NSS 10', 'ADHESIVO') : 'ADHESIVO ',
                ('CDB', 'CANDADO') : 'CANDADO ',
                ('CTA', 'CINTA') : 'CINTA METRICA ',
                ('DES 7', 'DEST') : 'DESTORNILLADOR ',
                ('DES 8P', 'DEST') : 'DESTORNILLADOR ',
                ('DES 8R', 'DEST') : 'DESTORNILLADOR ',
                ('DES 8T', 'DEST') : 'DESTORNILLADOR ',
                ('DSA ', 'DISCO') : 'DISCO ',
                ('DSD ', 'DISCO') : 'DISCO ',
                ('PST ', 'PISTOLA') :'PISTOLA ',
                ('C P', 'PISTOLA') : 'PISTOLA ',
                ('PZA P P', 'PINZA') :'PINZA ',
                ('ZNO', 'ZOCALO') : 'ZOCALO ',
                ('SR ', 'SERRUCHO') : 'SERRUCHO ',
                ('RM ', 'REMACHADORA') : 'REMACHADORA ',
                ('LLV 7C 22', 'LLAVE') : 'KIT LLAVE CRIQUET ',
                ('LLV C3/4', 'LLAVE') : 'LLAVE ',
                ('MT BMD 225', 'MARTILLO') : 'MARTILLO ',
                ('MT GMD 16', 'MARTILLO') : 'MARTILLO ',
                }

        for key,value in mapeo.items():
            condicion_1 = lista['codigo'].str.contains(key[0])
            condicion_2 = ~lista['detalle'].str.contains(key[1])
            condicion = condicion_1 & condicion_2
            lista.loc[condicion, 'detalle'] = value + lista['detalle']

        lista['distribuidora'] = distribuidora
        reemplazos = {'CANO' : 'CAÑO',
                        'P/CANO' : 'P/CAÑO',
                        'C/CANO ' : 'C/CAÑO',
                        'VULCAÑO' : 'VULCANO',
                        'VOLCAÑO' : 'VOLCANO',
                        'AMERICAÑO' : 'AMERICANO',
                        'AFRICAÑO' : 'AFRICANO',
                        '\n' : '', 
                        '\'' : '', 
                        '\"' : ''
                        }
        lista['detalle'] = lista['detalle'].replace(reemplazos, regex=True)

        if lista.shape[0]<3 or lista.shape[1]<3:
            return 'error'
        else:
            lista.to_csv(nombre_arch_csv, header= False, index= False)
            return nombre_arch_csv.split("\\")[1]
    
    except Exception as e:
        print(e)
        return 'error'

if __name__== "__main__":
    DISTRIBUIDORA= "SUPRABOND"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
