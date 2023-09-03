"""Este modulo se encarga de encontrar en la carpeta de archivos
normalizados todos los items que coinciden con el item buscado"""
import os
import csv


def crear_lista_archivos():
    """Esta funcion busca en el drectorio donde se encuentra el programa
    todos los archivos normalizados .csv y crea una lista con ellos"""
    lista_archivos = []
    ruta = os.getcwd() + "\\archivos_normalizados"
    contenido = os.listdir(ruta)
    for archivo in contenido:
        if archivo.endswith(".csv"):
            lista_archivos.append(archivo)
    return ruta, lista_archivos


def buscar_items(item_buscado):
    """Busca todas las coincidencia en los archivos que estan en la lista
    de archivos generada por el modulo Crear_lista de _archivos"""
    lista_coincidencias = []
    ruta, lista_archivos = crear_lista_archivos()
    item_buscado = item_buscado.upper().translate(item_buscado.maketrans('ÁÉÍÓÚÜ', 'AEIOUU'))

    for archivo in lista_archivos:
        try:
            with open(f"{ruta}\\{archivo}", "r", encoding='utf-8-sig') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    # -- busca coincidencias y filtra items con valor 0 en el precio
                    if item_buscado in row[1] and float(row[2]) != 0:
                        lista_coincidencias.append(row)
        except Exception as error:
            print(error)

    return lista_coincidencias


if __name__ == "__main__":
    lista = buscar_items("pincel")
    for item in lista:
        print(item)
