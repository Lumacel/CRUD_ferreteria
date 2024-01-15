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
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename

    if os.path.basename(file).startswith("GENERAL"):
        mapeo = ['CABLE DE ALUMINIO', 'CABLE DE COBRE', 'CAJAS ESTANCA',
                'CALENTADOR DE INMERSION', 'CINTA METRICA', 'FLEXIBLES',
                'FLEXIBLE MALLADO','FOTOCELULAS', 'LUCES DE EMERGENCIA',
                'LLAVE CIOCCA  EXTERIOR DE SUPERFICIE ', 'MULTIFICHAS',
                'SILICONA TRANSPARENTE ACÉTICA'
                ]

        lista = pd.read_csv(file)

        columnas = {lista.columns[0] : 'detalle',
                    lista.columns[1] : 'marca',
                    lista.columns[2] : 'precio'
                    }
        lista = lista.rename(columns= columnas)
        lista['codigo']= 'S/CODIGO'
        lista.loc[lista['marca'].notna(), 'detalle'] = lista['detalle']+' (' + lista['marca'] + ')'
        lista = lista[['codigo','detalle','precio']]
        categorias = lista[lista['precio'].isna()]
        categ_dic = categorias['detalle'].to_dict()
        indice_cat = list(categ_dic.keys())
        lista['precio']= pd.to_numeric(lista['precio'], errors= 'coerce')
        
        for indice in lista.index:
            for i in range(len(indice_cat)-1):
                if indice_cat[i] < indice < indice_cat[i+1] and categ_dic[indice_cat[i]] in mapeo:
                    lista.loc[indice,'detalle'] = categ_dic[indice_cat[i]] + ' ' + lista.loc[indice,'detalle']

    else:
        lista = pd.read_csv(file)
        columnas = {lista.columns[0] : 'codigo',
                    lista.columns[1] : 'detalle',
                    lista.columns[4] : 'precio'
                    }
        lista = lista.rename(columns= columnas)
        lista = lista[['codigo', 'detalle', 'precio']]
        lista['codigo'] = lista['codigo'].str.strip()
        lista['precio'] = pd.to_numeric(lista['precio'], errors= 'coerce')
        
    lista= lista.dropna()
    lista['precio'] = lista['precio'].round(2)
    lista['detalle'] = lista['detalle'].str.upper()
    # eliminando acentos, dieresis y caracteres no ascii
    lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
    lista['distribuidora'] = distribuidora
    mapeo_reemplazos = {'CANO' : 'CAÑO',
                        'P/CANO' : 'P/CAÑO',
                        'C/CANO ' : 'C/CAÑO',
                        'VULCAÑO' : 'VULCANO',
                        'AMERICAÑO' : 'AMERICANO',
                        'AFRICAÑO' : 'AFRICANO'
                        }
    for key,value in mapeo_reemplazos.items():
        lista['detalle'] = lista['detalle'].str.replace(key, value)
        
    lista.to_csv(nombre_arch_csv, header= False, index= False)

    return nombre_arch_csv.split("\\")[1]

if __name__=="__main__":
    DISTRIBUIDORA= "GUSTAVO_ELECT"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
