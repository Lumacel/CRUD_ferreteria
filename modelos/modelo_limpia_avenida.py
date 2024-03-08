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
    if "CAMBIOS" in file: ###### filtra hoja que tiene informacion sobre los cambios
        return None

    basename = os.path.basename(file)
    nombre_arch_csv = nombrar_archivo(distribuidora) + basename

    lista = pd.read_csv(file)

    try:
        columnas = {lista.columns[0] : 'codigo',
                    lista.columns[1]: 'detalle',
                    lista.columns[5] : 'precio'
                    }
        lista = lista.rename(columns= columnas)
        lista = lista[['codigo','detalle','precio']]
        # eliminando acentos, dieresis y caracteres no ascii
        lista['detalle'] = lista['detalle'].str.normalize('NFKD').str.encode('ASCII', 'ignore').str.decode('ASCII')
        lista['codigo'] = lista['codigo'].replace("", "S/CODIGO")
        lista['codigo'].fillna("S/CODIGO", inplace=True)
        lista['precio'] = pd.to_numeric(lista['precio'], errors='coerce')
        lista = lista.dropna()
        lista['precio'] = lista['precio'].round(2)
        lista['detalle'] = lista['detalle'].str.rstrip()
        lista['detalle'] = lista['detalle'].str.upper()
        reemplazos = {'\n':'', 
                      '\'':'', 
                      '\"':''
                      }
        lista['detalle'] = lista['detalle'].replace(reemplazos, regex=True)
        lista['distribuidora'] = distribuidora

        mapeo_codigos = {'L-3025|S-0166|S-017|S-019|S-028' : ['', ' (SANTA JUANA)'],
                        'E-0078|E0079' : ['', ' PARA MANGUERA'],
                        'M-05090|M-0928|R-00925' : ['', ' (EL ABUELO)'],
                        'A-0567|A-05680|A-05681|A-0569|A-0570' : \
                                ['PERCHAS AUTOADHESIVAS ', ' C/TORNILLOS'],
                        'A-0572|A-0593|A-0594' : ['', ' C/TORNILLOS'],
                        'A-056' : ['GANCHOS AUTOADHESIVOS ', ''],
                        'A-0593' : ['', ' PARA BAÑO - C/TORNILLOS'],
                        'E-006' : ['', ' PARA CORTINA'],
                        'P-110' : ['', ' (CRECCHIO)'],
                        'C-113' : ['', ' -PARA BORDEADORA-'],
                        'E-0106' : ['ESCALERA METALICA PLEGABLE ', ' (YAERCO)'],
                        'G-030' : ['GUANTES ', ''],
                        'P-0172' : ['PAPEL DE LIJA MADERA ', '-25 HOJAS- (HUNTER)'],
                        'L-0170' : ['LIJA AL AGUA ', ' (HUNTER)'],
                        'T-0350' : ['TELA DE ESMERIL ', ''],
                        'M-04015|M-0404|M-0405' : ['MAQUINA SALPICAR ', ''],
                        'S-0440' : ['', ' - POLIETILENO -'],
                        'S-0445|S-0446|S-0447' : ['SOGA TRENZADA ', ' - POLIPROPILENO -'],
                        'A-0149|A-0150|A-0151|A-0152|A-0153' : ['GRASA POTE ', '' ],
                        'A-0145|A-0146|A-0147|A-0148|A-0154|A-0155' : ['LUBRICANTE ', '' ],
                        'A-0138|A-0139' : ['ACEITERA CON BOMBA ', '' ],
                        'B-031' : ['BISAGRA CARPINTERO HIERRO ZINCADO ', '' ],
                        'B-03220' : ['BISAGRA FICHA HERRERO ', '' ],
                        'B-0320|0321' : ['BISAGRA HIERRO PULIDO REVERSIBLE ' , ''],
                        'B-033' : ['BISAGRA FICHA PARA PLACARDS ', ''],
                        'B-0371|B-0372|B-0373|B-0374' : \
                                ['BISAGRA MUNICION CON AGUJEROS HIERRO PULIDO ', ''],
                        'B-0375|B-0376|B-0377|B-0378|B-0379' : \
                                ['BISAGRA MUNICION SIN AGUJEROS HIERRO PULIDO ', ''],
                        'B-0380|0381' : ['BISAGRA HERRERO HIERRO PULIDO ', ''],
                        'B-041' : ['BISAGRA PARA POSTIGOS TIPO 1842 ', ' HIERRO PULIDO'],
                        'A-01655|A-01656' : ['SILICONA EN BARRA ', ''],
                        'A-05120' : ['ARCO SIERRA ', ''],
                        'B-3001|B-3002' : ['BISAGRAS ARMARIOS HIERRO BRONCEADO (CHINA) ', ''],
                        'B-2999|B-3000' : ['BISAGRAS ARMARIOS HIERRO PULIDO (CHINA) ', ''],
                        'C-13700|C-14000' : ['', ' -PARA MUEBLES-'],
                        'M-04971' : ['MARTILLO GALPONERO ', ''],
                        'P-0790' : ['PLOMADAS TRAZADORAS ', ''],
                        'S-036' : ['SIERRA CIRCULAR ', ''],
                        'S-0350|S-0351' : ['SIERRAS COPA BROCA ', ' RHEIN'],
                        'D-2310|D-2311' : ['DISCO DE CORTE DIAMANTADO ', ''],
                        'D-230' : ['DISCO DE CORTE DIAMANTADO ', ' YARD DHD'],
                        'H-019' : ['', ' PARA METALES'],
                        'H-021' : ['HOJA SIERRA ', ' PARA METALES'],
                        'H-022' : ['', ' PARA METALES'],
                        '&-1000' : ['',' - CON TRABA -'],
                        '&-1002' : ['',' - SIN TRABA -'],
                        'A-001|A-002|A-003' : ['ABRAZADERA A CREMALLERA ',''],
                        'A-007' : ['ABRAZADERA A TORNILLO ',''],
                        'M-060|M-061|M-062' : ['MECHA ACERO RAPIDO ',''],
                        'M-063' : ['MECHA ACERO RAPIDO DOBLEPUNTA ',''],
                        'M-069' : ['MECHA PUNTA DE WIDIA ',''],
                        'M-071' : ['MECHA ROTOPERCUTORA ',''],
                        'T-0141|T-0142' : ['TANZA DE NYLON PARA ALBAÑILES ', ''],
                        'T-0143|T-0144' : ['TANZA DE NYLON PARA BORDEADORAS ', ''],
                        'T-0148' : ['TANZA DE NYLON PARA PESCA ', ''],
                        'A-2403' : ['ALICATE CORTE OBLICUO AISLADO ', ''],
                        'L-3062' : ['LLAVES AJUSTABLES FOSFATIZADAS ', ''],
                        'P-06911|P-06912' : ['PINZA MEDIA CAÑA AISLADA ', ''],
                        'P-0692' : ['PINZA PICO DE LORO AISLADA ', ''],
                        'P-06914|P-06915' : ['PINZA PUNTA CHATA ', ''],
                        'P-06918' : ['PINZA PUNTA CURVA ', ''],
                        'P-0694' : ['PINZA ROSARIO PARA ARTESANIA ', ''],
                        'P-0697' : ['PINZA UNIVERSAL AISLADA', ''],
                        'T-0380' : ['TENAZA PARA ARMADORES AISLADAS ', ''],
                        'T-0391' : ['TENAZA PARA CARPINTEROS AISLADAS ', ''],
                        'P-0672' : ['PINCEL PINTOR CERDA BLANCA', 'ESSAMET'],
                        'L-0132' : ['LAPIZA PARA  CARPINTERO ', ''],
                        'L-304|L-305' : ['LLAVE EXAGONAL TIPO ALLEN ', ''],
                        'E-039' : ['ESQUINERO PLANO ', ''],
                        'D-0370|D-0371' : ['DESTORNILLADOR ', ' (METZ)'],
                        'D-0372|D-0373' : ['DESTORNILLADOR PHILLIPS ', ' (METZ)'],
                        'M-0770' : ['MENSULAS DE HIERRO CON COLGANTE', ' (CORVEX)'],
                        'S-0500' : ['', ' 10 ROLLITOS'],
                        'B-3050' : ['BISAGRAS PORTONES TIPO T ',''],
                        'T-048' : ['TENSORES PARA SOGAS Y TOLDOS GALVANIZADOS ', ''],
                        'C-220' : ['CORREDERAS PARA CAJONES DE MUEBLES ', ''],
                        }

        for key, value in mapeo_codigos.items():
            condicion = lista['codigo'].str.contains(key)
            lista.loc[condicion, 'detalle'] = value[0] + lista['detalle'] + value[1]
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

if __name__=="__main__":
    DISTRIBUIDORA= "LIMPIA_AVENIDA"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for archivo in open_files:
        normalizar_lista(archivo, DISTRIBUIDORA)
