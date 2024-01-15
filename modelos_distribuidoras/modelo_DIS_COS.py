
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
    """Realiza el trabajo de decodificar la lista para
    facilitar la busqueda de cada articulo"""
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file)

    columnas = {lista.columns[0] : 'codigo',
                lista.columns[1] : 'detalle',
                lista.columns[2] : 'precio',
                lista.columns[3] : 'marca'
                }
    lista = lista.rename(columns= columnas)
    lista['detalle'] = lista['detalle'].str.strip()
    lista['detalle'] = lista['detalle'] + ' (' + lista['marca'] + ')'
    lista = lista[['codigo', 'detalle', 'precio']]
    lista['detalle'] = lista['detalle'].str.upper()
    lista['precio'] = pd.to_numeric(lista['precio'], errors= 'coerce')
    # eliminando acentos, dieresis y caracteres no ascii
    lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
    lista = lista[lista['precio'] != 0]
    lista= lista.dropna()
    lista['precio'] = lista['precio'].round(2)
    lista['distribuidora'] = distribuidora
    mapeo_reemplazos = {'CANO' : 'CAÑO',
                        'P/CANO' : 'P/CAÑO',
                        'C/CANO ' : 'C/CAÑO',
                        'VULCAÑO' : 'VULCANO',
                        'VOLCAÑO' : 'VOLCANO',
                        'AMERICAÑO' : 'AMERICANO',
                        'AFRICAÑO' : 'AFRICANO'
                        }
    for key,value in mapeo_reemplazos.items():
        lista['detalle'] = lista['detalle'].str.replace(key, value)

    lista.to_csv(nombre_arch_csv, index= False, header= False)

    return nombre_arch_csv.split("\\")[1]

if __name__=="__main__":
    DISTRIBUIDORA= "DIS_COS"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
        