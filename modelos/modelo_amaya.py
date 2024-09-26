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
    """Agrega encabezado al nombre del archivo con la fecha y hora actual"""
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file)

    try:
        columnas = {lista.columns[0] : 'codigo',
                    lista.columns[1] : 'detalle',
                    lista.columns[3] : 'precio'
                    }
        lista= lista.rename(columns= columnas)

        lista['codigo']= lista['codigo'].astype(str)
        # eliminando acentos, dieresis y caracteres no ascii
        lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
        lista = lista[['codigo','detalle','precio']]
        lista['distribuidora'] = 'AMAYA'
        lista['precio'] = pd.to_numeric(lista['precio'], errors='coerce')
        lista= lista.dropna()
        lista['detalle'] = lista['detalle'].str.upper()
        lista['detalle'] = lista['detalle'].str.replace('\'','')
        lista['detalle'] = lista['detalle'].str.replace('\"','')
        lista['precio'] = lista['precio']*.558  # .558 coeficiente AMAYA (precio lista -38% -10%)
        lista['precio'] = lista['precio'].round(2)
        reemplazos = {'Ñ' : 'N',
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
    DISTRIBUIDORA = "AMAYA"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
        