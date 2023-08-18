import csv
import os
from datetime import datetime 
from tkinter import filedialog

def nombrar_archivo(distribuidora,carpeta="archivos_normalizados"):
    fecha = datetime.now()
    return f'{carpeta}\\{distribuidora}_{fecha.strftime("%Y-%m-%d_%H-%M-%S")}_'

def normalizar_lista(file, distribuidora):
    c=0
    basename = os.path.basename(file)
    nombre_arch_csv= nombrar_archivo(distribuidora) + basename
    try:
        with open(nombre_arch_csv, "a", newline="", encoding='utf-8-sig') as new_csvfile:
            writer_object= csv.writer(new_csvfile)
            with open(file, "r", encoding='utf-8-sig') as csvfile:
                spamreader= csv.reader(csvfile, delimiter=',')
                categoria= ""
               
                
                casos1 = ['CABLE DE ALUMINIO', 'CABLE DE COBRE', 'CAJAS ESTANCA', 
                          'CALENTADOR DE INMERSION', 'CINTA METRICA', 'FLEXIBLES', 'FLEXIBLE MALLADO', 
                          'FOTOCELULAS', 'LUCES DE EMERGENCIA', 'LLAVE CIOCCA  EXTERIOR DE SUPERFICIE ',
                          'MULTIFICHAS', 'SILICONA TRANSPARENTE ACÉTICA'
                          ]
                
                casos2= ['AUTOMATICOS PARA TANQUE ', 'BOLSA DE AGUA CALIENTE', 'BOMBA DE AGUA', 
                         'BURLETE DOBLE', 'BUSCAPOLO ', 'CAJAS CAPSULADAS', 'CAJAS DE HIERRO', 
                         'CAJAS PARA TERMICA (DE EMBUTIR Y EXTERIOR)', 'CAJA PVC', 'CALEFONES Y ACCESORIOS', 
                         'CALOVENTOR', 'CAMPANILLAS/ZUMBADORES', 'CONECTORES DE HIERRO', 'CONECTORES PVC', 
                         'CORDON DE PLANCHA/INTERLOCK', 'CURVA PVC', 'ESTAÑO EN BLISTER X 10 UNIDADES', 
                         'FICHAS 3P', 'FICHA ADAPTADOR / VELADOR', 'GAS BUTANO', 'GUIRNALDA', 
                         'INTERRUPTOR P/ESTUFA Y BORDEADORA', 'LAMPARA LED DICROICA', 
                         'LAMPARAS LED: GOTA / VELA', 'LAMPARA PERFUME INCANDESCENTE', 
                          'PARCHE PILETA', 'PORTALAMPARAS Y RECEPTACULOS', 
                         'PORTATIL ', 'PROLONGADORES', 'REGULADORES', 'SELLAROSCAS', 'SPOT DE DICROICAS', 
                         'TAPA AUTOADHESIVA', 'TAPA PVC A PRESIÓN/ TORNILLO', 'TEFLON', 'TIMMER ENCHUFABLE', 
                         'UNION PVC', 'VARIADORES ', 'ZAPATILLAS Y PROLONGADORES'
                         ]

                for row in spamreader:
                    if os.path.basename(file).startswith("GENERAL"):
                        if row[0] in casos1:
                            categoria= row[0]
                            continue
                       
                        elif row[0] in casos2:
                            categoria= ""
                            continue
                        try:
                            if len(row)<3 : continue
                            row = ["S/CODIGO", f"{categoria} {row[0]} [{row[1]}]", row[2]]
                            try:
                                row[2]= f"{float(row[2]):.2f}"
                            except Exception:
                                continue
                            row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                            row[1]=row[1].rstrip()
                            row.append(distribuidora)

                            c+= 1
                            writer_object.writerow(row)
                            print(c,row)
                        except Exception as e:
                            pass                  
                    else:
                        try:
                            try:
                                while True:
                                    row.remove('')
                            except Exception:
                                pass
                            try:
                                row[2]= f"{float(row[2]):.2f}"
                            except ValueError:
                                continue
                            row[1]= row[1].translate(row[1].maketrans('ÁÉÍÓÚÜ','AEIOUU'))
                            row[1]=row[1].rstrip()
                            row.append(distribuidora)   
                                
                            c+= 1
                            writer_object.writerow(row)
                            print(c,row)
                        except Exception as e:
                            pass                                             
    except Exception as e:
           print(e)
           
    return nombre_arch_csv.split("\\")[1]
  
if __name__=="__main__":
    distribuidora = "GUSTAVO_ELECT"
    open_files = filedialog.askopenfilenames(filetypes=[("Archivos Excel", "*.csv")])
    for file in open_files:
        normalizar_lista(file, distribuidora)
        


