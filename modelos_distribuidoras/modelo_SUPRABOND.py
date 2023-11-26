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

    columnas= {lista.columns[0] : 'codigo',
            lista.columns[1] : 'grupo',
            lista.columns[2] : 'marca',
            lista.columns[5] : 'presentacion',
            lista.columns[6] : 'tipo',
            lista.columns[8] : 'detalle',
            lista.columns[9] : 'precio'
            }
    lista = lista.rename(columns= columnas)
    lista['grupo'] = lista['grupo'].fillna(0)
    lista['presentacion'] = lista['presentacion'].fillna('.')
    lista = lista[columnas.values()] # seleccionamos columnas que formaran dataframe
    lista['detalle'] = lista['detalle'].str.normalize('NFKD')\
                    .str.encode('ASCII', 'ignore').str.decode('ASCII')
    lista[['presentacion', 'tipo', 'detalle']] =\
             lista[['presentacion', 'tipo', 'detalle']].apply(lambda x : x.str.upper())
    lista['detalle'] = lista['detalle'] + '  - ' + lista['presentacion'] +\
            ' (' + lista['marca'] + ')'
    lista = lista.dropna()

    mapeo = {'ADHESIVO DE CONTACTO ' : [100, "ADHESIVO DE CONTACTO"],
            'ADHESIVO EPOXI ' : [200, 'ADHESIVO EPOXI'],
            "BURLETE " : [800, "PISTOLA"],
            "PISTOLA APLICADORA " : [800, "PISTOLA"],
            "PISTOLA ENCOLADORA " : [850, "PISTOLA"],
            'SELLADOR ' : [1000, 'SELLADOR'],
            "TOPETINA " : [1300, "TOPETINA"],
            "ZOCALO " : [1400, "ZOCALO"],
            "CANDADO " : [2500, "CANDADO"],
            "DESTORNILLADOR " : [2900, 'x.x.x'],
            "DISCO ABRASIVO DE CORTE " : [3050, "DISCO ABRASIVO"],
            "DISCO ABRASIVO DE DESBASTE " : [3051, "DISCO ABRASIVO"],
            "DISCO DIAMANTADO " : [3000, "DISCO DIAMANTADO"],
            "ESPATULA " : [3200, "ESPATULA"],
            "LIMA SERIE 500 " : [3605, "LIMA"],
            "PINZA " : [4150, "PINZA"],
            "SERRUCHO " : [4700, "SERRUCHO"],
            "TIJERA " : [4300, "TIJERA"]}

    for key,value in mapeo.items():
        condicion_1 = lista['grupo'] == value[0]
        condicion_2 = ~lista['detalle'].str.contains(value[1])
        condicion = condicion_1 & condicion_2
        lista.loc[condicion, 'detalle'] = key + lista['detalle']

    lista['precio'] = lista['precio'].round(2)
    lista = lista[['codigo', 'detalle', 'precio']]
    lista['distribuidora'] = distribuidora

    lista.to_csv(nombre_arch_csv, header= False, index= False)

    return nombre_arch_csv.split("\\")[1]

if __name__== "__main__":
    DISTRIBUIDORA= "SUPRABOND"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
