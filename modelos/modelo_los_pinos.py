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
    nombre_arch_csv = nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file)

    try:
        lista = lista.astype(object)

        if lista.shape[0] < 75:
            return None

        columnas= {lista.columns[0] : 'detalle',
                    lista.columns[1] : 'precio',}
        lista = lista.rename(columns= columnas)

        # corre los campos hacia la izquierda donde hay lugares vacios
        for i in range(3):
            lista[lista['detalle'].isna()] = lista.shift(periods=-1, axis=1, fill_value=None)

        lista= lista.dropna(how= 'all')
        lista = lista[lista['precio'].notna()]
        lista = lista[~lista['precio'].str.contains('U')]
        lista = lista[['detalle', 'precio']]
        lista['precio'] = lista['precio'].str.strip(' $')
        lista['detalle'] = lista['detalle'].str.strip(' ')
        lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.\
                            encode('ASCII', 'ignore').str.decode('ASCII')

        condicion = lista['detalle'].str.contains('Pintor') | lista['detalle'].str.contains('Familiar')
        lista.loc[condicion, 'detalle'] = 'Escalera ' + lista['detalle'] + ' (' + lista['precio'] + ')'

        try:
            items = ['Escalon Familiar',
                    'Escalon Familiar 11-12',
                    'Escalon Pintor de 4 a 10',
                    'Escalon Pintor de 11 a 12',
                    'Escaleras']

            familiar_3_10 = lista.loc[lista['detalle'].str.contains(items[0]),
                                'precio'].astype(float).iloc[0]
            familiar_11_12 = lista.loc[lista['detalle'].str.contains(items[1]),
                                'precio'].astype(float).iloc[0]
            pint_4_10 = lista.loc[lista['detalle'].str.contains(items[2]),
                                'precio'].astype(float).iloc[0]
            pint_11_12 = lista.loc[lista['detalle'].str.contains(items[3]),
                                'precio'].astype(float).iloc[0]

            for item in items: # elimina las filas que tienen los precios de  escalones
                lista = lista.loc[~lista['detalle'].str.contains(item)]
            for escalones in range(3,13): #asigna los precios a escaleras familiar segun escalones
                cadena = f'Familiar de {escalones}'
                lista.loc[lista['detalle'].str.contains(cadena) , ['precio']] =\
                    str(escalones*familiar_3_10) if escalones < 11 else str(escalones*familiar_11_12)
            for escalones in range(4,13): #asigna los precios a escaleras pintor segun escalones
                cadena = f'Pintor de {escalones}'
                lista.loc[lista['detalle'].str.contains(cadena) , ['precio']] =\
                    str(escalones*pint_4_10) if escalones < 11 else str(escalones*pint_11_12)
        except IndexError:
            pass

        mapeo_items= {'Liviano|Pesado' : ['Ruberoi ', ''],
                    'Rollo lamiplas|Autoadhesiva de|Memb ' : ['Membrana ', ''],
                    'Motor|Tambor' : ['', ' (Repuesto para hormigonera)'],
                    'Maciza|Neumatica p/' : ['Rueda ', ''],
                    'Banqueta|Caballetes de Madera|Tabla|Banco' : ['', ' (Art. de pino)'],
                    'Electrico Aleman' : ['Calefon ', '']
                    }
        for key, value in mapeo_items.items():
            condicion = lista['detalle'].str.contains(key)
            lista.loc[condicion, 'detalle'] = value[0] + lista['detalle'] + value[1]

        # diferencia tipos de pintura
        index_pinturas = lista.loc[lista['detalle'].str.contains('Pintura Latex')].index
        for numero,indice in enumerate(index_pinturas):
            marca = ' (PREMIUM)' if numero < 7 else ' (LINEA DECOR) '
            lista.loc[indice,'detalle'] = lista.loc[indice,'detalle'] + marca

        try:
            # Separa valores en una misma linea transforma en 2 items independientes
            p_cab = lista.loc[lista['detalle'].str.contains('Caballetes'), 'precio'].str.split('/')
            p_cab_reforz = p_cab.iloc[0][0].strip('$')
            p_cab_comun = p_cab.iloc[0][1].strip('$')
            index_caba = p_cab.index[0]
            lista.loc[index_caba, 'precio'] = str(p_cab_comun)
            nueva_fila = pd.DataFrame({'detalle' : ['Caballetes de Madera reforzado (Art. de pino)'],
                                        'precio' : [str(p_cab_reforz)]})
            lista = pd.concat([lista.loc[:index_caba],nueva_fila,
                            lista.loc[index_caba + 1:]]).reset_index(drop=True)
        except IndexError:
            pass

        lista['detalle'] = lista['detalle'].str.upper()
        lista['detalle'] = lista['detalle'].str.replace('\'','')
        lista['detalle'] = lista['detalle'].str.replace('\"','')
        lista['precio'] = pd.to_numeric(lista['precio'], errors='coerce')
        lista['precio'] = lista['precio'].round(2)
        lista = lista.dropna()
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

        lista['codigo'] = 'S/CODIGO'
        lista['distribuidora'] = distribuidora
        lista = lista[['codigo','detalle','precio','distribuidora']]

        if lista.shape[0]<3 or lista.shape[1]<3:
                return 'error'
        else:
            lista.to_csv(nombre_arch_csv, header= False, index= False)
            return nombre_arch_csv.split("\\")[1]

    except Exception as e:
        print(e)
        return 'error'

if __name__== "__main__":
    DISTRIBUIDORA= "LOS_PINOS"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
        