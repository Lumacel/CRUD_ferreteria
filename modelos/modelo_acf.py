"""Este modulo crea un archivo .csv con la informacion que hay en
archivo original pero normaliza la cantidad de columnas y
corrige omisiones que pueden hacer dificil la busqueda de un articulo
"""
import os
from datetime import datetime
from tkinter import filedialog
import pandas as pd

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    """Agrega encabezado al nombre del archivo con la fecha y hora actual"""
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    """Reorganiza la lista para facilitar la busqueda de cada articulo"""

    if "Hoja 1" in file:  ##### FILTRA LA HOJA 1 PORQUE TIENE LA MISMA INFORMACION QUE LA HOJA 2
        return None

    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file, header= None, na_values=[0])

    try:
        columnas= {lista.columns[0]: 'codigo',
                    lista.columns[1] : 'detalle',
                    lista.columns[2]: 'marca',
                    lista.columns[3]: 'precio'
                    }
        lista = lista.rename(columns= columnas)
        # eliminando acentos, dieresis y caracteres no ascii
        lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
        lista['detalle'] = lista['detalle'].str.cat([' (' + lista['marca'] + ')'], sep='', na_rep='')
        lista['detalle'] = lista['detalle'].str.upper()

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
        lista['detalle'] = lista['detalle'].str.replace('\'','')
        lista['detalle'] = lista['detalle'].str.replace('\"','')
        lista['precio'] = pd.to_numeric(lista['precio'], errors= 'coerce')
        lista = lista.dropna()
        lista = lista[['codigo', 'detalle', 'precio']]
        lista['distribuidora'] = distribuidora
        lista['precio'] = lista['precio'].round(2)

        mapeo_codigos = {'G101|ONE|GD' : 'PINCEL ',
                        'ATG|EPG|CUB|ART|LH|LE1|LE2|LN2|SL|ESP1|ESP2|FOR|EP5|EP8|EP11|\
                        EP17|EP22|AT5|AT8|AT11|AT17|AT22' : 'RODILLO ',
                        }

        for key, value in mapeo_codigos.items():
            condicion = lista['codigo'].str.contains(key)
            lista.loc[condicion, 'detalle'] = value + lista['detalle']

        if lista.shape[0]<3 or lista.shape[1]<3:
            return 'error'
        else:
            lista.to_csv(nombre_arch_csv, header= False, index= False)
            return nombre_arch_csv.split("\\")[1]

    except Exception as e:
        print(e)
        return 'error'

if __name__== "__main__":
    DISTRIBUIDORA= "ACF"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        if archivo.endswith("Hoja 1.csv"):
            continue # ignora primer hoja de dist. ACF
        normalizar_lista(archivo, DISTRIBUIDORA)
    