"Este archivo contiene la clase venta"

import json
from datetime import datetime


class Ventas():
    """ Esta clase maneja todo lo que a la venta
    se refiere: items ingresados con sus valores y descuentos"""

    def __init__(self, codigo="", articulo="", cantidad=0,
                 descuento=0, precio=0, distribuidora=""):
        self.codigo_vta = codigo
        self.articulo_vta = articulo
        self.cantidad_vta = cantidad
        self.descuento_vta = descuento
        self.precio_vta = precio
        self.distribuidora_vta = distribuidora
        self.medio_pago = True
        self.desc_global_vta = 0
        self.coeficiente_vta = self.get_coeficiente_vta()
        self.total=0
        self.tarjeta=0
        self.efectivo=0
        self.items_vta = []  # almacena los objetos items a vender

    def registrar_porcentaje_ganancia(self, porcentaje):
        """Escribe en un archivo el porcentaje de ganancia
        que se está usando"""
        with open(r"remarcacion\\porcentaje.txt", "w", encoding="latin1") as archivo:
            archivo.write(str(porcentaje))

    def get_porcentaje_ganancia(self):
        """asigna el porcentaje 
        de ganancia que está guardado en el archivo
        remarcacion"""
        with open(r"remarcacion\\porcentaje.txt", "r", encoding="latin1") as archivo:
            valor = archivo.readline()
            try:
                porcentaje = float(valor)
                if 0 <= porcentaje <= 100:
                    return porcentaje
                return None
            except ValueError :
                return None

    def get_coeficiente_vta(self):
        """calcula el coeficiente de venta de acuerdo
        al porcentaje de ganancia estipulado"""
        coeficiente= 1 + self.get_porcentaje_ganancia()/100
        return coeficiente

    def modificar_medio_pago(self):
        """cambia el medio de pago
        de efectivo a tarjeta y viceversa"""
        self.medio_pago = not self.medio_pago

    def agregar_item(self, item):
        """Agrega un nuevo item a la venta"""
        self.items_vta.append(item)

    def borrar_item(self, index=-1):
        """borra item seleccionado en
        la interfaz tkinter"""
        self.items_vta.pop(index)

    def descuento_global(self, descuento):
        """agrega un descuento a todos los items
        de la venta en curso"""
        self.desc_global_vta = descuento
        for item in self.items_vta:
            item.descuento_vta = abs(descuento)

    def editar_articulo(self, item, nuevos_valores):
        """edita el articulo con los cambios hechos
        en la interfaz tkinter"""
        item.cantidad_vta = abs(int(nuevos_valores['cant']))
        item.articulo_vta = nuevos_valores['art']
        item.precio_vta = f"{abs(nuevos_valores['prec']/nuevos_valores['frac']):.2f}"
        item.descuento_vta = f"{abs(nuevos_valores['desc']):.2f}"

    def calc_total_vta(self):
        """calcula el total de la venta sumando 
        todos los items y restando los descuentos"""
        total_vta, total_desc = 0, 0
        for item in self.items_vta:
            total_item = int(item.cantidad_vta)*float(item.precio_vta)
            descuento = float(item.descuento_vta)
            descuento_item = total_item*descuento/100
            total_vta += total_item
            total_desc += descuento_item

        self.total = total_vta - total_desc
        return self.total

    def discriminar_forma_pago(self, monto_tarjeta=0):
        """discrimina cuanto en efectivo y cuantocon tarjeta se
          paga cuando el pago no es con un solo medio"""
        if self.medio_pago:
            self.tarjeta = round(monto_tarjeta, 2)
            self.efectivo = round(self.calc_total_vta(), 2)
        else:
            self.tarjeta = round(monto_tarjeta, 2)
            self.efectivo = round((self.total-self.tarjeta), 2)
        self.grabar_venta()

    def grabar_venta(self):
        """registra en archivo registro_ventas
        una nueva venta en formato json"""
        lista_articulos = []
        values = []
        campos = ["codigo", "articulo", "cantidad",
                  "descuento", "precio", "distribuidora"]

        # - Guarda numero de venta
        with open(r"numeracion_ventas\\numeracion.txt", "r+", encoding="latin1") as archivo:
            numeracion = archivo.readline()
            nuevo_num = int(numeracion)+1
            archivo.seek(0)
            nuevo_num = str(nuevo_num).rjust(8, "0")
            archivo.writelines(str(nuevo_num))

        for item in self.items_vta:
            values = [str(item.codigo_vta),
                      item.articulo_vta,
                      int(item.cantidad_vta),
                      float(item.descuento_vta),
                      float(item.precio_vta),
                      item.distribuidora_vta
                      ]
            
            articulos = dict(zip(campos, values)) # genera diccionario

            lista_articulos.append(articulos)

        fecha = datetime.now()
        time_stamp = datetime.timestamp(fecha)

       # Datos de nueva venta
        nueva_venta = {"timestamp": time_stamp,
                       "numeracion": nuevo_num,
                       "estado": True,
                       "efectivo": abs(self.efectivo),
                       "tarjeta": abs(self.tarjeta),
                       "articulos": lista_articulos
                       }

        # - Agrega venta al archivo json
        with open(r"registro_ventas\\ventas.json", "r+", encoding='utf-8-sig') as file:
            data = json.load(file)
            data.append(nueva_venta)
            file.seek(0)
            json.dump(data, file, indent=4)

        self.reiniciar_valores_vta()

    def reiniciar_valores_vta(self):
        """una vez hecha la venta reinicia 
        valores para una nueva venta"""
        self.items_vta = []
        self.medio_pago = True
        self.desc_global_vta = 0
