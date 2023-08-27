import csv
import os


def crear_lista_archivos():
    lista_archivos = []
    ruta = os.getcwd() + "\\archivos_normalizados"
    contenido = os.listdir(ruta)
    for archivo in contenido:
        if archivo.endswith(".csv"):
            lista_archivos.append(archivo)
    return ruta, lista_archivos


def buscar_items(item):
    lista_coincidencias = []
    ruta, lista_archivos = crear_lista_archivos()
    item = item.upper().translate(item.maketrans('ÁÉÍÓÚÜ', 'AEIOUU'))

    for archivo in lista_archivos:
        try:
            with open(f"{ruta}\\{archivo}", "r", encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    # -- busca coincidencias y filtra items con valor 0 en el precio
                    if item in row[1] and float(row[2]) != 0:
                        lista_coincidencias.append(row)
        except Exception as e:
            print(e)

    return lista_coincidencias


if __name__ == "__main__":
    lista = buscar_items("pincel")
    for item in lista:
        print(item)
