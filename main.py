""" En este archivo se aloja el programa principal
 y la clase que controla la interfaz grafica tkinter"""
import json
import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import Calendar
import buscador
import conversor
import normalizador
from ventas import Ventas

class App():
    """Crea y gestiona la interfaz gráfica"""
    def __init__(self):
        self.distribuidoras =  self.cargar_distribuidoras()
        self.distr_selecc = "TODAS"
        self.ventas = Ventas() # pone clase Venta como instancia de la clase App
        self.ventana_principal()

    def cargar_distribuidoras(self):
        """Carga las distribuidoras de un archivo de textos"""
        distribuidoras = []
        try:
            with open(r"distribuidoras\distribuidoras.csv", "r", encoding="latin1") as csvfile:
                spamreader = csv.reader(csvfile)
                for i in spamreader:
                    distribuidoras.append(i[0])
                distribuidoras.sort()
                distribuidoras.insert(0,"TODAS")
                return distribuidoras
        except Exception:
            messagebox.showinfo(message="ERROR!!! NO SE PUDIERON CARGAR LAS DISTRIBUIDORAS",
                                title="INFO")
            return None

    def centrar_ventana(self,ancho_ventana,alto_ventana):
        """Da una posicion para centrar una ventana de acuerdo a sus dimensioness"""
        ancho_pantalla= self.root.winfo_screenwidth()
        alto_pantalla=self.root.winfo_screenheight()
        x_ventana = ancho_pantalla // 2 - ancho_ventana // 2
        y_ventana = alto_pantalla // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        return posicion

    def ventana_principal(self):
        """Crea ventana principal donde estarán los items a vender"""
        ancho_ventana= 1200
        alto_ventana= 320

        self.root = tk.Tk()
        self.root.title("FERRETERIA")
        self.root.resizable(0,0)

        # -- agrega estilo
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.root.geometry(posicion)

        # --aloja el menú
        self.menu()

        self.articulo_busq = tk.StringVar()
        self.distr_selecc= tk.StringVar()

        self.lbl_buscar = tk.Label(self.root, text="  BUSCAR ARTICULO  ", relief= "ridge",
                                   width= 20, bg= "lightblue", fg= "black",font=("Arial", 11))
        self.lbl_buscar.place(x=12,y=10)
        self.entry_buscar = tk.Entry(self.root,textvariable = self.articulo_busq, width=74,
                                     font=("Arial", 11))
        self.entry_buscar.place(x=200,y=10)
        self.lbl_distr = tk.Label(self.root, text = "DISTRIBUIDORA", width=20, relief= "ridge",
                                  bg= "lightblue" ,fg= "black", font=("Arial", 11))
        self.lbl_distr.place(x=814, y=10)
        self.entry_distr = ttk.Combobox(self.root,textvariable = self.distr_selecc,
                                        values=self.get_distribuidoras(), state="readonly",
                                        width=20, height=len(self.get_distribuidoras()))
        self.entry_distr.place(x=1002,y=10)
        self.entry_distr.config(font=("Arial", 11))

        self.subtotal = tk.DoubleVar()
        self.descuento = tk.DoubleVar()
        self.total = tk.DoubleVar()

        self.lbl_modo_pago = tk.Label(self.root, text= "-- EFECTIVO --", relief= "sunken",
                                      width=24, bg= "lightblue", fg= "blue",justify = "right",
                                      font=("Arial", 11))
        self.lbl_modo_pago.place(x=25,y=260)
        self.lbl_subtotal_name = tk.Label(self.root, text = "SUBTOTAL ", relief= "ridge",
                                          width=12, bg= "lightblue", fg= "black",
                                          font=("Arial", 11))
        self.lbl_subtotal_name.place(x=328,y=260)
        self.lbl_subtotal_valor = tk.Label(self.root, textvariable = self.subtotal,
                                           relief= "sunken", width=12,
                                           bg= "white", fg= "black",justify = "right",
                                           font=("Arial", 11))
        self.lbl_subtotal_valor.place(x=443,y=260)
        self.lbl_descuento_name = tk.Label(self.root, text="DESCUENTO ", relief= "ridge",
                                            width= 12, bg= "lightblue", fg= "black",
                                            font=("Arial", 11))
        self.lbl_descuento_name.place(x=627,y=260)
        self.lbl_descuento_valor = tk.Label(self.root, textvariable= self.descuento,
                                            relief= "sunken",width= 12, bg= "white",
                                            fg= "black", justify = "right",
                                            font=("Arial", 11))
        self.lbl_descuento_valor.place(x=743,y=260)
        self.lbl_total_name = tk.Label(self.root, text="A PAGAR ", relief= "ridge", width= 12,
                                       bg= "lightblue", fg= "black",font=("Arial", 11))
        self.lbl_total_name.place(x=918,y=260)
        self.lbl_total_valor = tk.Label(self.root, textvariable= self.total, relief= "sunken",
                                        width= 12, bg= "white", fg= "black", justify = "right",
                                        font=("Arial", 11))
        self.lbl_total_valor.place(x=1033,y=260)

        # eventos asociados
        self.root.bind("<<ComboboxSelected>>", lambda x : self.buscar_item()
                       if self.get_articulo_busq() else None)
        self.root.bind("<Control-Delete>", lambda x: self.borrar_items_vta()
                       if self.tabla_venta.selection() else self.entry_buscar.focus() )
        self.root.bind("<Return>", lambda x: self.return_root())
        self.root.bind("<Double-Button-1>", lambda x : self.editar_item_vta("EDITAR") if
                        self.tabla_venta.selection() else self.entry_buscar.focus())
        self.root.bind("<Control-r>", lambda x : self.resetear_venta())
        self.root.bind("<Escape>", lambda x :  self.escape_root())
        self.root.bind("<F2>", lambda x: self.aceptar_venta() if self.ventas.items_vta else None)
        self.root.bind("<F3>", lambda x:self.ver_archivos_normalizados())
        self.root.bind("<F4>", lambda x:self.toplevel_normalizar())
        self.root.bind("<F5>", lambda x: self.toplevel_dto_global())
        self.root.bind("<F6>", lambda x: self.toplevel_ganancia())
        self.root.bind("<F7>", lambda x: self.toplevel_registros())
        self.root.bind("<F8>", lambda x : self.modif_medio_pago())
        self.root.bind("<F10>", lambda x : self.editar_item_vta("AGREGAR"))

        # -- Nuevo frame dentro de la raiz(root)
        self.frame = tk.Frame(self.root,bg= "lightgrey", relief="ridge",bd=4)
        self.frame.place(x=10,y=40)
        self.frame.configure(width=1178, height=212)

        self.entry_buscar.focus()
        self.entry_distr.set("TODAS")

        self.treeview_venta()
        self.cargar_treeview_venta()

    def menu(self):
        """Crea el menú que irá alojado en la raiz"""

        # --Crea el menú Archivo
        menu_archivo = tk.Menu(self.root, tearoff= False, font=("Arial", 11))
        menu_archivo.add_command(label="Explorar archivos", accelerator="F3",
                                      command= self.ver_archivos_normalizados)
        menu_archivo.add_command(label="Normalizar listas", accelerator="F4",
                                      command= self.toplevel_normalizar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)

        # Crear el menú Editar
        menu_ventas = tk.Menu(self.root, tearoff= False, font=("Arial", 11))
        menu_ventas.add_command(label="Efectuar venta", accelerator="F2",
                                     command= lambda : self.aceptar_venta()
                                     if self.ventas.items_vta else None)
        menu_ventas.add_command(label="Aplicar descuento global", accelerator="F5",
                                     command= self.toplevel_dto_global)
        menu_ventas.add_command(label="Agregar artículo", accelerator="F10",
                                     command= lambda: self.editar_item_vta("AGREGAR"))
        menu_ventas.add_command(label="Editar artículo", accelerator="Enter",
                                     command= lambda: self.editar_item_vta("EDITAR")
                                     if self.tabla_venta.selection() else None)
        menu_ventas.add_command(label="Borrar artículo/s", accelerator="Ctrl + Del",
                                     command= self.borrar_items_vta )
        menu_ventas.add_command(label="Modificar medio de pago", accelerator="F8",
                                     command= self.modif_medio_pago)
        menu_ventas.add_command(label="Reiniciar venta", accelerator="Ctrl + R",
                                     command= self.resetear_venta)

        # --Crea el menú Configuración
        menu_config = tk.Menu(self.root, tearoff= False, font=("Arial", 11))
        menu_config.add_command(label="Modificar margen ganancia", accelerator="F6",
                                     command= self.toplevel_ganancia)
        menu_config.add_command(label="Registros historicos", accelerator="F7",
                                     command= self.toplevel_registros)

        # --Crea la barra de menús y agregar los menús
        barra_menus = tk.Menu(self.root)

        barra_menus.add_cascade(label="   Archivos", menu=menu_archivo)
        barra_menus.add_cascade(label=" Ventas", menu=menu_ventas)
        barra_menus.add_cascade(label=" Configuración", menu=menu_config)

        # --Agrega la barra de menús a la ventana
        self.root.config(menu=barra_menus)

    def toplevel_ganancia(self):
        """Abre una ventana dondse se podrá cambiar el porcentaje de ganancia"""
        ancho_ventana= 278
        alto_ventana= 140

        self.toplevel_gan = tk.Toplevel()
        self.toplevel_gan.title("GANANCIA")
        self.toplevel_gan.resizable(0,0)
        self.toplevel_gan.focus_force()
        self.toplevel_gan.grab_set()

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_gan.geometry(posicion)

        self.password = tk.StringVar()
        self.porcentaje_ganancia = tk.DoubleVar()
        self.porcentaje_ganancia.set(self.ventas.get_porcentaje_ganancia())

        self.lbl_ganancia = tk.Label(self.toplevel_gan,text="GANANCIA % ", bg = "lightblue",
                                     relief= "ridge", width= 13, font=("Arial", 11))
        self.lbl_ganancia.place(x=12, y= 20)
        self.entry_ganancia = tk.Entry(self.toplevel_gan,textvariable = self.porcentaje_ganancia,
                                       width=15,justify = "right", font=("Arial", 11))
        self.entry_ganancia.place(x=138,y=20)
        self.lbl_clave = tk.Label(self.toplevel_gan,text="CONTRASEÑA", bg = "lightblue",
                                  relief= "ridge", width= 13, font=("Arial", 11))
        self.lbl_clave.place(x=12, y= 60)
        self.entry_clave = tk.Entry(self.toplevel_gan,textvariable = self.password,
                                    show="*", width=15,justify = "right", font=("Arial", 11))
        self.entry_clave.place(x=138,y=60)
        self.btn_ganancia_aceptar = tk.Button(self.toplevel_gan, text= " ACEPTAR " , width = 10,
                                              command= lambda: self.cambiar_valor_ganancia(),
                                              font=("Arial", 11))
        self.btn_ganancia_aceptar.place(x= 12, y= 100)
        self.btn_ganancia_salir = tk.Button(self.toplevel_gan, text= " SALIR " , width = 10,
                                            command= lambda: self.toplevel_gan.destroy(),
                                            font=("Arial", 11))
        self.btn_ganancia_salir.place(x= 162, y= 100)

        self.entry_ganancia.focus()
        self.entry_ganancia.select_range(0, 'end')
        self.entry_ganancia.icursor('end')

        self.toplevel_gan.bind("<Return>", lambda x: self.cambiar_valor_ganancia())
        self.toplevel_gan.bind("<Escape>", lambda x : self.toplevel_gan.destroy())

    def cambiar_valor_ganancia(self):
        """Verifica si el valor ingresado es válido y en
        ese caso lo cambia por el nuevo"""
        mensaje_except = "POR FAVOR REVISE LOS DATOS INGRESADOS\n    LOS DOS CAMPOS SON OBLIGATORIOS"
        try:
            porc_gan= float(self.porcentaje_ganancia.get())
            if 0<= porc_gan <=100 and self.password.get()== "Tango2023":
                self.toplevel_gan.destroy()
                messagebox.showinfo(message=f"  EL PORCENTAJE DE GANANCIA AHORA ES {porc_gan}%  ",
                                    title="INFO")
                self.ventas.registrar_porcentaje_ganancia(porc_gan)
                self.ventas.coeficiente_vta= self.ventas.get_coeficiente_vta()
            else:
                self.resetear_level_ganancia()
                messagebox.showinfo(message=mensaje_except, title="INFO")
        except:
            self.resetear_level_ganancia()
            messagebox.showinfo(message= mensaje_except, title="INFO")

    def resetear_level_ganancia(self):
        """ resetea los valores del toplevel ganancia """
        self.entry_ganancia.focus()
        self.entry_ganancia.select_range(0, 'end')
        self.entry_ganancia.icursor('end')

    def modif_medio_pago(self):
        """Cambia la forma de pago entre tarjeta y efectivo"""
        if messagebox.askyesno(title="MEDIO DE PAGO",
                               message= "PAGO CON TARJETA" if self.ventas.medio_pago else "PAGO EN EFECTIVO" ):
            self.ventas.modificar_medio_pago()
            self.lbl_modo_pago.config(text = "-- EFECTIVO --" if self.ventas.medio_pago else "-- TARJETA --")
        else:
            pass

    def return_root(self):
        """verifica desde donde se presiona el ENTER para realizar búsqueda
        si el foco está en el entry de busqueda o abrir el toplevel de
        edicion con los datos del item seleccionado si esta seleccionado 
        algun articulo"""
        if isinstance(self.root.focus_get(), tk.Entry):
            self.buscar_item()
        else:
            if self.tabla_venta.selection():
                self.editar_item_vta("EDITAR")
            else:
                pass

    def escape_root(self):
        """Ajusta parametros cuando se presiona la tecla esc:
           -deselecciona items previamente seleccionados
           -borra palabra clave de busqueda 
           -enfoca en el entry de busqueda
           -selecciona todas las distribuidoras"""
        self.tabla_venta.selection_remove(*self.tabla_venta.selection())
        self.entry_buscar.delete("0","end")
        self.entry_buscar.focus()
        self.entry_distr.set("TODAS")

    def toplevel_dto_global(self):
        """ Crea ventana donde se puede seleccionar un
        descuento global para todos los items"""
        ancho_ventana= 278
        alto_ventana= 100

        self.toplevel_dto = tk.Toplevel()
        self.toplevel_dto.title("DTO. GLOBAL")
        self.toplevel_dto.resizable(0,0)
        self.toplevel_dto.focus_force()
        self.toplevel_dto.grab_set()

        self.dto_global = tk.DoubleVar()

        self.dto_global.set(self.get_dto_global())

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_dto.geometry(posicion)

        self.lbl_dto = tk.Label(self.toplevel_dto,text="DESCUENTO %", bg = "lightblue",
                                relief= "ridge", width= 13, font=("Arial", 11))
        self.lbl_dto.place(x=12, y= 20)
        self.entry_dto = tk.Entry(self.toplevel_dto,textvariable = self.dto_global , width=15,
                                  justify = "right", font=("Arial", 11))
        self.entry_dto.place(x=138,y=20)
        self.btn_dto_aceptar = tk.Button(self.toplevel_dto, text= " ACEPTAR ", width = 10,
                                         command= lambda :self.aplicar_dto_global(),
                                         font=("Arial", 11))
        self.btn_dto_aceptar.place(x= 12, y= 60)
        self.btn_dto_salir = tk.Button(self.toplevel_dto, text= " SALIR ", width = 10,
                                       command= lambda : self.toplevel_dto.destroy() ,
                                       font=("Arial", 11))
        self.btn_dto_salir.place(x= 162, y= 60)

        self.entry_dto.focus()
        self.entry_dto.select_range(0, 'end')
        self.entry_dto.icursor('end')

        self.toplevel_dto.bind("<Return>", lambda x: self.aplicar_dto_global())
        self.toplevel_dto.bind("<Escape>", lambda x : self.toplevel_dto.destroy())

    def aplicar_dto_global(self):
        try:
            descuento = float(self.dto_global.get())
            if 0 <= descuento <= 100:
                self.ventas.descuento_global(descuento)
                self.toplevel_dto.destroy()
                self.cargar_treeview_venta()
            else:
                messagebox.showinfo(message="SOLO SE PERMITEN VALORES NUMERICOS (0-100)",
                                    title="INFO")
                self.dto_global.set(self.get_dto_global())
                self.entry_dto.focus()
                self.entry_dto.select_range(0, 'end')
                self.entry_dto.icursor('end')
        except Exception:
            messagebox.showinfo(message="SOLO SE PERMITEN VALORES NUMERICOS (0-100)",
                                title="INFO")
            self.dto_global.set(self.get_dto_global())
            self.entry_dto.focus()
            self.entry_dto.select_range(0, 'end')
            self.entry_dto.icursor('end')

    def toplevel_resultados(self):
        """Abre ventana para mostrar los resultados de la busqueda"""
        ancho_ventana= 1150
        alto_ventana = 260

        self.toplevel_result = tk.Toplevel()
        self.toplevel_result.focus_force()
        self.toplevel_result.resizable(0,0)
        self.toplevel_result.title("RESULTADOS")

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_result.geometry(posicion)

        self.lbl_distr_resultados = tk.Label(self.toplevel_result, text = "DISTRIBUIDORA",
                                             width=20, relief= "ridge", bg= "lightblue",
                                             fg= "black", font=("Arial", 11))
        self.lbl_distr_resultados.place(x=745, y=210)
        self.lbl_item_resultados = tk.Label(self.toplevel_result, text= "BUSQUEDA",
                                            relief= "ridge", width= 20,bg= "lightblue",
                                            fg= "black", font=("Arial", 11))
        self.lbl_item_resultados.place(x=12,y=210)
        self.entry_item_resultados = tk.Label(self.toplevel_result,
                                              text = (self.articulo_busq.get()).upper(),
                                              relief= "sunken", width=20, font=("Arial", 11))
        self.entry_item_resultados.place(x=200,y=210)
        self.entry_distr_resultados = ttk.Combobox(self.toplevel_result,
                                                   textvariable = self.distr_selecc,
                                                   values=self.get_distribuidoras(),
                                                   state="readonly", width=20,
                                                   height=len(self.get_distribuidoras()))
        self.entry_distr_resultados.place(x=933,y=210)
        self.entry_distr_resultados.config(font=("Arial", 11))

        self.toplevel_result.grab_set() # --- inhabilita controles ventana principal

        self.toplevel_result.bind("<<ComboboxSelected>>", lambda x : self.combobox_select())
        self.toplevel_result.bind("<Escape>", lambda x: self.esc_toplevel_resultados())
        self.toplevel_result.bind("<Return>", lambda x: self.agregar_artic_venta())
        self.toplevel_result.bind("<Double-Button-1>", lambda x : self.agregar_artic_venta())
        self.toplevel_result.protocol("WM_DELETE_WINDOW", self.esc_toplevel_resultados)

        self.treeview_busqueda()
        self.cargar_treeview_resultados()

    def esc_toplevel_resultados(self):
        """ Ajusta los parametros de la ventana principal
            cuando se sale del toplevel_resultados"""
        self.toplevel_result.destroy()
        self.distr_selecc.set("TODAS")
        self.entry_buscar.focus_set()
        self.entry_buscar.select_range(0, 'end')
        self.entry_buscar.icursor('end')

    def combobox_select(self):
        """ actualiza el treeview del toplevel_resultados
            cuando se cambia la distribuidora en el combobox"""
        self.tabla_resultados.delete(*self.tabla_resultados.get_children())
        self.cargar_treeview_resultados()

    def treeview_busqueda(self,filas=8):
        """Da formato al treeview donde apareceran
        los items que coinciden con la busqueda"""
        columnas= ("CODIGO","ARTICULO","P. COMPRA $","P. VENTA $","DISTRIBUIDORA")
        self.tabla_resultados = ttk.Treeview(self.toplevel_result, height=filas,
                                             show="headings", columns=columnas)
        self.tabla_resultados.place(x= 10 , y=10)

		# --- barra scroll
        self.scroll = tk.Scrollbar(self.toplevel_result, orient="vertical",
                                   command=self.tabla_resultados.yview)
        self.scroll.place(x=1120, y=28, height=166)
        self.tabla_resultados.configure(yscrollcommand=self.scroll.set)

		# --- formato a las columnas
        #self.tabla_resultados.column("#0", width=0, stretch=tk.NO , minwidth=100)
        self.tabla_resultados.column("CODIGO", anchor=tk.W, width=100, minwidth = 120)
        self.tabla_resultados.column("ARTICULO", anchor=tk.W, width=640, minwidth = 620)
        self.tabla_resultados.column("P. COMPRA $", anchor=tk.E, width=100, minwidth = 100)
        self.tabla_resultados.column("P. VENTA $", anchor=tk.E, width=100, minwidth = 100)
        self.tabla_resultados.column("DISTRIBUIDORA", anchor=tk.CENTER, width=155,minwidth = 155)

		# --- indicar cabecera
        #self.tabla_resultados.heading("#0", text="", anchor=tk.W)
        self.tabla_resultados.heading("#1", text="CODIGO", anchor=tk.CENTER)
        self.tabla_resultados.heading("#2", text="ARTICULO", anchor=tk.CENTER)
        self.tabla_resultados.heading("#3", text="P. COMPRA $", anchor=tk.CENTER)
        self.tabla_resultados.heading("#4", text="P. VENTA $", anchor=tk.CENTER)
        self.tabla_resultados.heading("#5", text="DISTRIBUIDORA", anchor=tk.CENTER)

    def treeview_venta(self, filas = 8 ):
        """Da el formato al treeview de la ventana principal
        donde se sitúan los items seleccionados"""
        columnas= ("ARTICULO", "CANT.", "PRECIO", "SUBTOTAL", "DTO. %","DTO. $", "TOTAL")
        self.tabla_venta = ttk.Treeview(self.root, height=filas, show="headings", columns=columnas)
        self.tabla_venta.place(x= 25 , y=50)

        self.style.configure("Treeview", font=("Arial", 11))
        self.style.configure('Treeview.Heading', background="lightblue", foreground="black",
                             font=("Arial", 11))

        self.scroll_venta = tk.Scrollbar(self.root, orient="vertical",
                                         command=self.tabla_venta.yview)
        self.scroll_venta.place(x=1160, y=74, height=161)
        self.tabla_venta.configure(yscrollcommand=self.scroll_venta.set)

        #self.tabla_venta.column("#0", width=0, stretch=tk.NO , minwidth=100)
        self.tabla_venta.column("ARTICULO", anchor=tk.W, width=570, minwidth = 570)
        self.tabla_venta.column("CANT.", anchor=tk.CENTER, width=50, minwidth = 50)
        self.tabla_venta.column("PRECIO", anchor=tk.E, width=100, minwidth = 100)
        self.tabla_venta.column("SUBTOTAL", anchor=tk.E, width=100, minwidth = 100)
        self.tabla_venta.column("DTO. %", anchor=tk.E, width=100, minwidth =100)
        self.tabla_venta.column("DTO. $", anchor=tk.E, width=100, minwidth = 100)
        self.tabla_venta.column("TOTAL", anchor=tk.E, width=100, minwidth = 100)

		# --- indicar cabecera
        #self.tabla_venta.heading("#0", text="", anchor=tk.CENTER)
        self.tabla_venta.heading("#1", text="ARTICULO", anchor=tk.CENTER)
        self.tabla_venta.heading("#2", text="CANT.", anchor=tk.CENTER)
        self.tabla_venta.heading("#3", text="PRECIO", anchor=tk.CENTER)
        self.tabla_venta.heading("#4", text="SUBTOTAL", anchor=tk.CENTER)
        self.tabla_venta.heading("#5", text="DTO. %", anchor=tk.CENTER)
        self.tabla_venta.heading("#6", text="DTO. $", anchor=tk.CENTER)
        self.tabla_venta.heading("#7", text="TOTAL", anchor=tk.CENTER)

    def cargar_treeview_resultados(self):
        """Carga el treeview con los items que 
        coinciden con la búsqueda """
        for item in self.lista_coincidencias:
            if item[3] == self.get_distr_selecc() or self.get_distr_selecc() == "TODAS":
                codigo = item[0]
                articulo = item[1]
                precio_compra = f'{float(item[2]):.2f}'
                precio_venta = f"{(float(item[2])*self.ventas.coeficiente_vta):.2f}"
                distribuidora = item[3]
                lista = (codigo, articulo, precio_compra, precio_venta, distribuidora)
                self.tabla_resultados.insert("", tk.END, text="", values=lista)
            else:
                continue

    def agregar_artic_venta(self):
        """Agrega los items seleccionados en la ventana
           de resultados que da la búsqueda"""
        items_selecc = self.tabla_resultados.selection()  # items selecc(marcados en azul)
        if len(items_selecc)>0:
            for i in items_selecc:
                item = self.tabla_resultados.item(i)["values"]

                nuevo_artic = Ventas(item[0],
                           item[1],
                           1,
                           self.get_dto_global(),
                           item[3],
                           item[4]
                           )  # crea objeto Ventas

                self.ventas.agregar_item(nuevo_artic)  # agrega objeto a la lista

        self.cargar_treeview_venta()
        self.articulo_busq.set("")
        self.distr_selecc.set("TODAS")
        self.entry_buscar.focus()

    def cargar_treeview_venta(self):
        """Carga los datos de los archivos seleccionados para la venta"""
        subtotales= 0
        descuentos= 0
        totales= 0

        self.reiniciar_valores()

        for item in self.ventas.items_vta:
            articulo = item.articulo_vta
            cantidad = int(item.cantidad_vta)
            precio = float(item.precio_vta)
            descuento = float(item.descuento_vta)
            subtotal = precio*cantidad
            total_desc= subtotal*descuento/100
            total= subtotal - total_desc
            subtotales+= subtotal
            descuentos+= total_desc
            totales+= total

            lista = (articulo,
                     cantidad,
                     f"{precio:.2f}",
                     f"{subtotal:.2f}",
                     f"{descuento:.2f} %",
                     f"{total_desc:.2f}",
                     f"{total:.2f}"
                     )

            self.tabla_venta.insert("", tk.END, text="", values=lista)

        # -- cargar lbls al pie de root
        self.subtotal.set(f" {subtotales:.2f}".rjust(16," "))
        self.descuento.set(f" {descuentos:.2f}".rjust(16," "))
        self.total.set(f" {totales:.2f}".rjust(16," "))
        try:
            self.toplevel_result.destroy()
        except:
            pass
        self.articulo_busq.set("")

    def borrar_items_vta(self):
        """Elimina los items seleccionados"""
        items_selecc = self.tabla_venta.selection()  # items seleccionados (marcados en azul)
        items = self.tabla_venta.get_children()  # Devuelve tupla con los id de elementos
        compensador=-1
        for i in items_selecc:
            compensador+= 1
            posicion = items.index(i)-compensador
            self.ventas.borrar_item(posicion)
        self.cargar_treeview_venta()

    def editar_item_vta(self,modo):
        """asigna modo EDITAR o modo AGREGAR  """
        self.modo = modo
        self.toplevel_editar()

    def resetear_venta(self):
        """reinicia valores para una nueva venta"""
        self.ventas.reiniciar_valores_vta()
        self.lbl_modo_pago.config(text = "-- EFECTIVO --" )
        self.cargar_treeview_venta()

    def toplevel_editar(self):
        """Abre ventana para editar item seleccionado"""
        ancho_ventana = 778
        alto_ventana = 100

        self.ventana_editar = tk.Toplevel()
        self.ventana_editar.title(self.modo + " ARTICULO")
        self.ventana_editar.resizable(0,0)

        posicion = self.centrar_ventana(ancho_ventana, alto_ventana)
        self.ventana_editar.geometry(posicion)

        self.cant_editar = tk.IntVar()
        self.artic_editar = tk.StringVar()
        self.precio_editar = tk.DoubleVar()
        self.dto_editar = tk.DoubleVar()
        self.fracc_editar = tk.IntVar()
        self.fracc_state = tk.BooleanVar()

        self.lbl_cant_editar= tk.Label(self.ventana_editar, text = "CANT.", relief= "ridge",
                                       width = 5, bg= "lightblue", font=("Arial", 11))
        self.lbl_cant_editar.place(x=1,y=5)
        self.lbl_artic_editar= tk.Label(self.ventana_editar, text = "ARTICULO", relief= "ridge",
                                        width = 58, bg= "lightblue", font=("Arial", 11))
        self.lbl_artic_editar.place(x=52,y=5)
        self.lbl_artic_precio= tk.Label(self.ventana_editar, text = "PRECIO $", relief= "ridge",
                                        width = 12, bg= "lightblue", font=("Arial", 11))
        self.lbl_artic_precio.place(x=580,y=5)
        self.lbl_artic_descuento= tk.Label(self.ventana_editar, text = "DTO. %", relief= "ridge",
                                           width = 8, bg= "lightblue", font=("Arial", 11))
        self.lbl_artic_descuento.place(x=694,y=5)
        self.entry_cant_editar= tk.Entry(self.ventana_editar, textvariable = self.cant_editar,
                                         width = 6, bg= "white", justify = "center",
                                         font=("Arial", 11))
        self.entry_cant_editar.place(x=1,y=28)
        self.entry_artic_editar= tk.Entry(self.ventana_editar, textvariable = self.artic_editar,
                                          width = 66, bg= "white", justify = "left",
                                          font=("Arial", 11))
        self.entry_artic_editar.place(x=52,y=28)
        self.entry_artic_precio= tk.Entry(self.ventana_editar, textvariable = self.precio_editar,
                                          width = 14, bg= "white", justify = "right",
                                          font=("Arial", 11))
        self.entry_artic_precio.place(x=580,y=28)
        self.entry_artic_descuento= tk.Entry(self.ventana_editar, textvariable = self.dto_editar ,
                                             width = 9, bg= "white", justify = "right",
                                             font=("Arial", 11))
        self.entry_artic_descuento.place(x=694,y=28)
        self.lbl_fraccionar = tk.Label(self.ventana_editar, text = "FRACCIONAR", relief= "ridge",
                                       width = 12, state= "disabled", bg= "lightblue",
                                       font=("Arial", 10))
        self.lbl_fraccionar.place(x=5,y=70)
        self.entry_fraccionar = tk.Entry(self.ventana_editar, textvariable = self.fracc_editar,
                                         width = 5,state= "disabled", bg= "white",
                                         justify = "right", font=("Arial", 11))
        self.entry_fraccionar.place(x=110,y=70)
        self.check_btn_fracc = ttk.Checkbutton(self.ventana_editar, text = "Habilitar",
                                               variable = self.fracc_state,
                                               command= self.fracc_seleccion)
        self.check_btn_fracc.place(x=160,y=70)

        self.fracc_editar.set(1)
        self.ventana_editar.grab_set()

        if self.modo== "EDITAR":
            focus_item = self.tabla_venta.focus()
            items = self.tabla_venta.get_children()
            index = items.index(focus_item)
            item = self.ventas.items_vta[index]
            self.precio_original= item.precio_vta  # guarda el precio inicial del producto
        else:
            item = Ventas("S/COD.", "", 1, "0.00", "0.00","LOCAL") #add item con valores nulos
            self.ventas.agregar_item(item)

        self.cant_editar.set(item.cantidad_vta)
        self.artic_editar.set(item.articulo_vta)
        self.precio_editar.set(item.precio_vta)
        self.dto_editar.set(item.descuento_vta)

        self.reset_campo_cantidad()

        self.ventana_editar.event_generate("<Button-1>") # simula un click para activar ventana

        self.ventana_editar.bind("<Escape>", lambda x: self.escape_editar())
        self.ventana_editar.bind("<Return>", lambda x: self.validar_entradas(item))
        self.ventana_editar.bind("<KeyRelease>", lambda x: self.key_released_fracc ())
        self.ventana_editar.protocol("WM_DELETE_WINDOW", self.escape_editar) # cuando se cierra la ventana

    def fracc_seleccion(self):
        """Permite o no fraccionar el producto cuando se selecciona fraccionar"""
        if self.fracc_state.get():
            self.entry_fraccionar.config(state= "normal")
            self.lbl_fraccionar.config(state= "normal")
        else:
            self.entry_fraccionar.config(state= "disabled")
            self.lbl_fraccionar.config(state= "disabled")

    def key_released_fracc(self):
        """actualiza precio cada vez que se ingresa un valor de fraccion"""
        if self.fracc_state.get():
            try:
                precio = self.precio_editar.get()
                fraccion= self.fracc_editar.get()
                fraccion = int(fraccion)
                precio = self.precio_original
                precio_fracc = round(float(precio)/fraccion,2)
                self.precio_editar.set(precio_fracc)
            except:
                self.fracc_editar.set("1")
                self.precio_editar.set(self.precio_original)
                self.entry_fraccionar.focus()
                self.entry_fraccionar.select_range(0, 'end')
                self.entry_fraccionar.icursor('end')
            else:
                pass

    def validar_entradas(self,item):
        """Valida entrada de datos al editar o agregar """
        try:
            articulo= (self.artic_editar.get()).upper()
            cantidad = int(self.cant_editar.get())
            precio = round((float(self.precio_original if self.fracc_state.get() else self.precio_editar.get())),2)
            fraccion = int(self.fracc_editar.get())
            descuento = float(self.dto_editar.get())
            if cantidad == 0 or descuento< 0 or descuento> 100 or precio<= 0 or articulo== "":
                messagebox.showinfo(message="VERIFIQUE QUE LOS VALORES INGRESADOS SEAN CORRECTOS",
                                    title="INFO")
                self.reset_campo_cantidad()
            else:
                nuevos_valores= {"art":articulo,
                                 "cant":cantidad,
                                 "prec":precio,
                                 "frac":fraccion,
                                 "desc":descuento
                                 }
                self.ventas.editar_articulo(item, nuevos_valores)
                self.ventana_editar.destroy()
                self.cargar_treeview_venta()
                self.entry_buscar.focus()
        except Exception:
            messagebox.showinfo(message="VERIFIQUE QUE LOS VALORES INGRESADOS SEAN CORRECTOS",
                                title="INFO")
            self.reset_campo_cantidad()

    def reset_campo_cantidad(self):
        """Posiciona cursor en el campo cantidad y selecciona valor"""
        self.entry_cant_editar.select_range(0, 'end')
        self.entry_cant_editar.icursor('end')
        self.entry_cant_editar.focus()

    def escape_editar(self):
        """Sale del toplevel_editar y elimina el objeto venta que
        se habia creado para editar si estaba abierto en modo agregar."""
        if self.modo == "AGREGAR":
            self.ventas.borrar_item()
        else:
            pass
        self.ventana_editar.destroy()

    def buscar_item(self):
        """Busca en los archivos normalizados coincidencias con la clave
        que pone el usuario para la búsqueda"""
        articulo = self.get_articulo_busq()
        if len(articulo)>2:
            print("Articulo:", articulo)
            self.lista_coincidencias = buscador.buscar_items(articulo)

            if len(self.lista_coincidencias)==0:
                messagebox.showinfo(message="NO HAY COINCIDENCIAS PARA SU BÚSQUEDA",
                                    title="INFO")
                self.entry_buscar.select_range(0, 'end')
                self.entry_buscar.icursor('end')
            else:
                self.toplevel_resultados()
                for item in self.lista_coincidencias:
                    print(item)
        else:
            messagebox.showinfo(message="LA BÚSQUEDA DEBE CONTENER AL MENOS 3 CARACTERES",
                                title="INFO")

    def toplevel_normalizar(self):
        """Abre ventana para seleccionar archivo y distribuidora a la que pertenece para
        normalizarlo"""
        lista_distr = list(self.get_distribuidoras())
        lista_distr.remove("TODAS")

        ancho_ventana = 400
        alto_ventana = 100

        self.ventana_normalizar = tk.Toplevel()
        self.ventana_normalizar.title("NORMALIZAR LISTA")
        self.ventana_normalizar.resizable(0,0)
        self.ventana_normalizar.focus_force()
        self.ventana_normalizar.grab_set()

        posicion = self.centrar_ventana(ancho_ventana, alto_ventana)
        self.ventana_normalizar.geometry(posicion)

        self.modelo_distr_norm = tk.StringVar()

        self.lbl_modelo = tk.Label(self.ventana_normalizar,text=" SELECCIONAR MODELO ",
                                   bg = "lightblue", relief= "ridge", width= 22,
                                   font=("Arial", 11))
        self.lbl_modelo.place(x=10, y= 20)
        self.entry_modelo = ttk.Combobox(self.ventana_normalizar,
                                         textvariable = self.modelo_distr_norm, values=lista_distr,
                                         state="readonly", width=18, height=len(lista_distr))
        self.entry_modelo.place(x=220,y=20)
        self.entry_modelo.config(font=("Arial", 11))
        self.btn_aceptar = tk.Button(self.ventana_normalizar, text= " ARCHIVO " , width = 10,
                                     command= self.normalizar_lista, font=("Arial", 11))
        self.btn_aceptar.place(x= 10, y= 60)
        self.btn_salir = tk.Button(self.ventana_normalizar, text= " SALIR ",width = 10,
                                   command= lambda : self.ventana_normalizar.destroy(),
                                   font=("Arial", 11))
        self.btn_salir.place(x= 288, y= 60)

        self.btn_aceptar.bind("<Return>", lambda x: self.normalizar_lista())
        self.btn_salir.bind("<Return>", lambda x: self.ventana_normalizar.destroy())
        self.ventana_normalizar.bind("<Escape>", lambda x: self.ventana_normalizar.destroy())
        self.entry_modelo.bind("<<ComboboxSelected>>", lambda x: self.btn_aceptar.focus())

    def toplevel_pago_tarjeta(self):
        """Abre ventana para poner el monto que se paga con tarjeta"""
        ancho_ventana= 278
        alto_ventana= 65

        self.toplevel_tarjeta = tk.Toplevel()
        self.toplevel_tarjeta.title("PAGO TARJETA")
        self.toplevel_tarjeta.resizable(0,0)
        self.toplevel_tarjeta.focus_force()
        self.toplevel_tarjeta.grab_set()

        self.monto_tarjeta = tk.DoubleVar()

        total= round(self.ventas.calc_total_vta(),2)

        self.monto_tarjeta.set(total)

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_tarjeta.geometry(posicion)

        self.lbl_tarjeta = tk.Label(self.toplevel_tarjeta,text="TARJETA",
                                    bg= "lightblue", relief= "ridge", width= 13,
                                    font=("Arial", 11))
        self.lbl_tarjeta.place(x=12, y= 20)
        self.entry_monto = tk.Entry(self.toplevel_tarjeta,textvariable = self.monto_tarjeta,
                                    width=15,justify = "right", font=("Arial", 11))
        self.entry_monto.place(x=138,y=20)

        self.entry_monto.focus()
        self.entry_monto.select_range(0, 'end')
        self.entry_monto.icursor('end')

        self.toplevel_tarjeta.bind("<Return>", lambda x: self.validar_monto_tarjeta())
        self.toplevel_tarjeta.bind("<Escape>", lambda x : self.toplevel_tarjeta.destroy())

    def aceptar_venta(self):
        """Pregunta si realmente quiere hacer la venta y nos lleva
        al toplevel que permite discriminar el pago"""
        if messagebox.askyesno(title="VENTA" , message = "EFECTUAR LA VENTA?"):
            self.escape_root()
            if self.ventas.medio_pago:
                self.reiniciar_valores()
                self.ventas.discriminar_forma_pago()
            else:
                self.toplevel_pago_tarjeta()
        else:
            pass

    def validar_monto_tarjeta(self):
        """Verifica que el monto de pago con tarjeta sea válido"""
        total_venta = round(self.ventas.calc_total_vta(),2)

        monto_tarj = float(self.monto_tarjeta.get())
        if  monto_tarj > total_venta or monto_tarj < 0:
            messagebox.showinfo(message="MONTO INVALIDO", title="INFO")
            self.reiniciar_valores_tarjeta()
        else:
            self.registrar_venta_tarjeta()

    def registrar_venta_tarjeta(self):
        """una vez que se verifica el monto de pago con tarjeta se registar la venta"""
        self.toplevel_tarjeta.destroy()
        self.reiniciar_valores()
        self.ventas.discriminar_forma_pago(self.monto_tarjeta.get())
        self.lbl_modo_pago.config(text = "-- EFECTIVO --")

    def reiniciar_valores_tarjeta(self):
        """reinicia valores de tarjeta originles cuando al elegir un monto no
        puede ser validado como correcto"""
        self.monto_tarjeta.set(round(self.ventas.calc_total_vta(),2))
        self.entry_monto.focus()
        self.entry_monto.select_range(0, 'end')
        self.entry_monto.icursor('end')

    def reiniciar_valores(self):
        """reinicia valores en ventana principal una vez hecha laventa"""
        self.tabla_venta.delete(*self.tabla_venta.get_children()) # borra registros treeview
        self.subtotal.set(f" {0:.2f}".rjust(16," "))
        self.descuento.set(f" {0:.2f}".rjust(16," "))
        self.total.set(f" {0:.2f}".rjust(16," "))

    def toplevel_registros(self):
        """Abre ventana para mostrar los registros segun fecha seleccionada"""
        ancho_ventana= 1165
        alto_ventana = 500

        self.toplevel_reg = tk.Toplevel()
        self.toplevel_reg.focus_force()
        self.toplevel_reg.resizable(0,0)
        self.toplevel_reg.title("REGISTROS")
        self.toplevel_reg.grab_set()

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_reg.geometry(posicion)

        self.toplevel_reg.grab_set() # --- inhabilita controles ventana principal

        fecha = datetime.now().strftime("%d-%m-%Y")

        self.fecha_inicial= tk.StringVar(value = fecha)
        self.fecha_final= tk.StringVar(value = fecha)

        self.lbl_fecha_inicial = tk.Label(self.toplevel_reg, text="DESDE", relief= "ridge",
                                          width=9, bg= "lightblue", fg= "black", font=("Arial", 10))
        self.lbl_fecha_inicial.place(x=12,y=10)
        self.entry_fecha_inicial = tk.Entry(self.toplevel_reg,textvariable = self.fecha_inicial,
                                            width=10, font=("Arial", 11))
        self.entry_fecha_inicial.place(x=92,y=10)
        self.lbl_fecha_final = tk.Label(self.toplevel_reg, text = "HASTA", width=9, relief= "ridge",
                                        bg= "lightblue" ,fg= "black", font=("Arial", 10))
        self.lbl_fecha_final.place(x=200, y=10)
        self.entry_fecha_final = tk.Entry(self.toplevel_reg, textvariable = self.fecha_final,
                                          width=10, font=("Arial", 11))
        self.entry_fecha_final.place(x=280,y=10)
        self.lbl_relleno = tk.Label(self.toplevel_reg, text = "", width=45, relief= "ridge",
                                    bg= None ,fg= "black", font=("Arial", 10))
        self.lbl_relleno.place(x=398, y=10)
        self.btn_estado_vta= tk.Button(self.toplevel_reg,text= "INCLUIR / ANULAR", width= 20,
                                       command = self.cambiar_estado_venta)
        self.btn_estado_vta.place(x=798,y=8)
        self.btn_resumen_vta= tk.Button(self.toplevel_reg,text=" VER RESUMEN VENTAS ",
                                        width= 20, command = self.toplevel_resumen_ventas)
        self.btn_resumen_vta.place(x=984,y=8)
        self.separator_1h = ttk.Separator(self.toplevel_reg, orient="horizontal")
        self.separator_1h.place(x=0, y=39, relwidth=1, anchor="w")

        self.lbl_title_ventas= tk.Label(self.toplevel_reg, text="Ventas",
                                        font=("Arial", 10))
        self.lbl_title_ventas.place(x= 12, y=45)

        self.separator_2h = ttk.Separator(self.toplevel_reg, orient="horizontal")
        self.separator_2h.place(x=0, y=302, relwidth=1, anchor="w")

        self.lbl_title_detalle= tk.Label(self.toplevel_reg, text="Detalle",
                                         font=("Arial", 10)).place(x= 12, y=308)
        self.entry_fecha_inicial.config(state="readonly",disabledforeground="black")
        self.entry_fecha_final.config(state="readonly",disabledforeground="black")

        self.entry_fecha_inicial.bind("<Button-1>", lambda x: self.set_modo_fecha_inicial())
        self.entry_fecha_final.bind("<Button-1>", lambda x: self.set_modo_fecha_final())
        self.toplevel_reg.bind("<Escape>", lambda x: self.esc_toplevel_reg())

        self.treeview_archivo()
        self.treeview_archivo_detalle()
        self.validar_fechas()

    def esc_toplevel_reg(self):
        """Evita bug. Al intentar cerrar la ventana calendario con un bind
        toma el bind escape de la ventana padre(toplevel_reg)"""
        try:
            if self.tl_calendario.winfo_viewable():
                self.tl_calendario.destroy()
            else:
                self.toplevel_reg.destroy()
        except Exception:
            self.toplevel_reg.destroy()

    def set_modo_fecha_inicial(self):
        """cuando se presiona boton para elegir fecha inicial en ventana de registros
        se setea la variable modo_fecha en 'inicial' """
        self.modo_fecha = "inicial"
        self.toplevel_calendario()

    def set_modo_fecha_final(self):
        """cuando se presiona boton para elegir fecha final en ventana de registros
        se setea la variable modo_fecha en 'final' """
        self.modo_fecha = "final"
        self.toplevel_calendario()

    def toplevel_calendario(self):
        """abre ventana tkcalendario para seleccionar fecha"""
        ancho_ventana= 300
        alto_ventana= 300

        self.tl_calendario = tk.Toplevel()
        self.tl_calendario.focus_force()
        self.tl_calendario.resizable(0,0)
        self.tl_calendario.title("CALENDARIO")

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.tl_calendario.geometry(posicion)

        self.tl_calendario.grab_set()

        day = datetime.now().strftime("%d")
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%Y")

        self.calend = Calendar(self.tl_calendario, selectmode = 'day',
               year = int(year), month = int(month),
               day = int(day),date_pattern="dd-mm-yyyy")
        self.calend.pack(pady = 20)

        self.btn_calend= tk.Button(self.tl_calendario, text = "ACEPTAR",
            command = self.seleccion_fecha).pack(pady = 20)

        self.tl_calendario.bind("<Escape>", lambda x: self.tl_calendario.destroy())
        self.tl_calendario.bind("<Return>", lambda x: self.seleccion_fecha())

    def seleccion_fecha(self):
        """Discrimina si la fecha seleccionada es final o inicial segun el modo activo"""
        fecha = self.calend.get_date()
        self.tl_calendario.destroy()

        if self.modo_fecha== "inicial":
            self.fecha_inicial.set(fecha)
        else:
            self.fecha_final.set(fecha)
        self.validar_fechas()

    def validar_fechas(self):
        """Verifica que las fechas sean correlativas"""
        ts_inicio,ts_final= self.get_fechas_seleccionadas()
        if ts_final<ts_inicio:
            messagebox.showinfo(message="POR FAVOR VERIFIQUE LAS FECHAS !!!",
                                title="INFO", parent=self.toplevel_reg)
        else:
            self.explorar_archivo_ventas(ts_inicio,ts_final)

    def explorar_archivo_ventas(self,ts_inicio,ts_final):
        """busca en el archivo las ventas comprendidas entre las fechas seleccionadas"""
        self.ventas_selecc=[]
        with open(r"registro_ventas\\ventas.json", "r", encoding='utf-8-sig') as file:
            data = json.load(file)
            for registro in data:
                if registro["timestamp"]>= ts_inicio and registro["timestamp"]<=ts_final:
                    self.ventas_selecc.append(registro)
                else: continue
        self.cargar_treeview_archivo()

    def treeview_archivo(self,filas=10):
        """configura treeview para ver registros de archivo"""
        columnas= ("FECHA", "HORA", "NUMERACION", "EFECTIVO", "TARJETA", "TOTAL", "ESTADO")
        self.tabla_archivo = ttk.Treeview(self.toplevel_reg, height=filas,show="headings",
                                          selectmode="browse", columns=columnas) # "browse" una fila
        self.tabla_archivo.place(x= 12 , y=70)

        self.scroll_archivo = tk.Scrollbar(self.toplevel_reg, orient="vertical",
                                           command=self.tabla_archivo.yview)
        self.scroll_archivo.place(x=1140, y=94, height=200)
        self.tabla_archivo.configure(yscrollcommand=self.scroll_archivo.set)

        #self.tabla_archivo.column("#0", width=0, stretch=tk.NO , minwidth=160)
        self.tabla_archivo.column("FECHA", anchor=tk.CENTER, width=160, minwidth = 160)
        self.tabla_archivo.column("HORA", anchor=tk.CENTER, width=160, minwidth = 160)
        self.tabla_archivo.column("NUMERACION", anchor=tk.CENTER, width=160, minwidth = 160)
        self.tabla_archivo.column("EFECTIVO", anchor=tk.E, width=160, minwidth = 160)
        self.tabla_archivo.column("TARJETA", anchor=tk.E, width=160, minwidth =160)
        self.tabla_archivo.column("TOTAL", anchor=tk.E, width=160, minwidth = 160)
        self.tabla_archivo.column("ESTADO", anchor=tk.CENTER, width=160, minwidth =160)

		# --- indicar cabecera
        #self.tabla_archivo.heading("#0", text="", anchor=tk.CENTER)
        self.tabla_archivo.heading("#1", text="FECHA", anchor=tk.CENTER)
        self.tabla_archivo.heading("#2", text="HORA", anchor=tk.CENTER)
        self.tabla_archivo.heading("#3", text="NUMERACION", anchor=tk.CENTER)
        self.tabla_archivo.heading("#4", text="EFECTIVO", anchor=tk.CENTER)
        self.tabla_archivo.heading("#5", text="TARJETA", anchor=tk.CENTER)
        self.tabla_archivo.heading("#6", text="TOTAL", anchor=tk.CENTER)
        self.tabla_archivo.heading("#7", text="ESTADO", anchor=tk.CENTER)

        self.tabla_archivo.bind("<<TreeviewSelect>>", lambda x: self.seleccionar_item_archivo())

    def cargar_treeview_archivo(self):
        """Carga treeview con los datos de las ventas correspondientes al lapso de fechas"""
        # columnas= ("FECHA", "HORA", "NUMERACION", "EFECTIVO", "TARJETA", "TOTAL", "ESTADO")
        self.vaciar_treeviews_registro()

        for item in self.ventas_selecc:
            dataframe =  datetime.fromtimestamp(item["timestamp"])
            fecha= dataframe.strftime("%d-%m-%Y")
            hora= dataframe.strftime("%H:%M:%S")
            numeracion= item["numeracion"]
            total= item["efectivo"] + item["tarjeta"]
            efectivo= item["efectivo"]
            tarjeta = item["tarjeta"]
            estado = chr(10004) if item["estado"] else chr(10005)

            lista = (fecha,
                     hora,
                     numeracion,
                     f"{efectivo:.2f}",
                     f"{tarjeta:.2f}",
                     f"{total:.2f}",
                     estado
                     )
            self.tabla_archivo.insert("", tk.END, text="", values=lista)

    def treeview_archivo_detalle(self,filas=6):
        """Organiza un treeview con los datos que tendrá el detalle de la venta"""
        columnas= ("CODIGO", "ARTICULO", "CANT.", "PRECIO", "SUBTOTAL",
                   "DTO. %","DTO. $", "TOTAL","DISTRIB.")
        self.tabla_archivo_detalle = ttk.Treeview(self.toplevel_reg, show="headings",
                                                  height=filas, columns=columnas)
        self.tabla_archivo_detalle.place(x= 12, y=332)

        self.scroll_archivo_detalle = tk.Scrollbar(self.toplevel_reg, orient="vertical",
                                                   command=self.tabla_archivo_detalle.yview)
        self.scroll_archivo_detalle.place(x=1140, y=355, height=125)
        self.tabla_archivo_detalle.configure(yscrollcommand=self.scroll_archivo_detalle.set)

        #self.tabla_archivo_detalle.column("#0", width=0, stretch=tk.NO , minwidth=100)
        self.tabla_archivo_detalle.column("CODIGO", anchor=tk.W, width=95, minwidth = 95)
        self.tabla_archivo_detalle.column("ARTICULO", anchor=tk.W, width=415, minwidth = 415)
        self.tabla_archivo_detalle.column("CANT.", anchor=tk.CENTER, width=50, minwidth = 50)
        self.tabla_archivo_detalle.column("PRECIO", anchor=tk.E, width=95, minwidth = 95)
        self.tabla_archivo_detalle.column("SUBTOTAL", anchor=tk.E, width=95, minwidth = 95)
        self.tabla_archivo_detalle.column("DTO. %", anchor=tk.E, width=70, minwidth =70)
        self.tabla_archivo_detalle.column("DTO. $", anchor=tk.E, width=70, minwidth = 70)
        self.tabla_archivo_detalle.column("TOTAL", anchor=tk.E, width=95, minwidth = 95)
        self.tabla_archivo_detalle.column("DISTRIB.", anchor=tk.CENTER, width=135, minwidth = 135)

		# --- indicar cabecera
        #self.tabla_archivo_detalle.heading("#0", text="", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#1", text="CODIGO", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#2", text="ARTICULO", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#3", text="CANT.", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#4", text="PRECIO", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#5", text="SUBTOTAL", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#6", text="DTO. %", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#7", text="DTO. $", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#8", text="TOTAL", anchor=tk.CENTER)
        self.tabla_archivo_detalle.heading("#9", text="DISTRIB.", anchor=tk.CENTER)

    def seleccionar_item_archivo(self):
        """Busca el detalle cuando un item es seleccionado en el treeview de ventas registadas"""
        elementos = self.tabla_archivo.get_children()
        seleccion = self.tabla_archivo.selection()
        try:
            indice = elementos.index(seleccion[0])
            self.cargar_treeview_archivo_detalle(indice)
        except:
            pass

    def cargar_treeview_archivo_detalle(self,indice):
        """muestra el detalle de la venta seleccionada en el registro"""
        #columnas= ("CODIGO", "ARTICULO", "CANT.", "PRECIO $", "SUBTOTAL $", "DTO. %","DTO. $", "TOTAL $")"""
        self.tabla_archivo_detalle.delete(*self.tabla_archivo_detalle.get_children())

        for item in self.ventas_selecc[indice]["articulos"]:
            codigo= item["codigo"]
            articulo= item["articulo"]
            cantidad= item["cantidad"]
            precio= item["precio"]
            subtotal= cantidad*precio
            desc_porc= item["descuento"]
            desc_pesos= cantidad*precio*desc_porc/100
            total= subtotal-desc_pesos
            distribuidora= item["distribuidora"]

            lista = (codigo,
                     articulo,
                     cantidad,
                     f"{precio:.2f}",
                     f"{subtotal:.2f}",
                     f"{desc_porc:.2f} %",
                     f"{desc_pesos:.2f}",
                     f"{total:.2f}",
                     distribuidora
                     )
            self.tabla_archivo_detalle.insert("", tk.END, text="", values=lista)

    def vaciar_treeviews_registro(self):
        """Elimina datos del treeview registro"""
        self.tabla_archivo.delete(*self.tabla_archivo.get_children())
        self.tabla_archivo_detalle.delete(*self.tabla_archivo_detalle.get_children())

    def ver_archivos_normalizados(self):
        """ Abre la carpeta donde estan alojados 
        todos los archivos .csv que se normalizaron a partir
        de las listas excel de las distribuidoras"""
        ruta = os.getcwd() + "\\archivos_normalizados"
        archivos = filedialog.askopenfilenames(initialdir=ruta,
                                               filetypes=[("Archivos Excel", "*.csv")])
        print(archivos)
        if archivos:
            for i in archivos:
                os.startfile(i)
        else:
            pass

    def toplevel_resumen_ventas(self):
        """ Crea una ventana flortate con el 
        resumen de todas las ventas comprendidas
        entre las fechas seleccionadas """
        ancho_ventana= 340
        alto_ventana = 230

        self.toplevel_resumen = tk.Toplevel()
        self.toplevel_resumen.focus_force()
        self.toplevel_resumen.resizable(0,0)
        self.toplevel_resumen.title("RESUMEN VENTAS")
        self.toplevel_resumen.grab_set()

        posicion = self.centrar_ventana(ancho_ventana,alto_ventana)
        self.toplevel_resumen.geometry(posicion)

        totales= self.resumen_vtas()

        total_bruto= totales["total_bruto"]
        total_descuentos= totales["total_descuentos"]
        total_ventas= totales["total_ventas"]
        total_efectivo= totales["total_efectivo"]
        total_tarjeta= totales["total_tarjeta"]
        cantidad_ventas= totales["cantidad_ventas"]

        fecha_inicial= self.fecha_inicial.get()
        fecha_final= self.fecha_final.get()

        self.lbl_fecha_txt = tk.Label(self.toplevel_resumen,
                                      text= f"Desde  {fecha_inicial}  hasta  {fecha_final}",
                                      font=("Arial", 12))
        self.lbl_fecha_txt.grid(row=0, column=0,columnspan=2)
        self.separador1 = tk.Label(self.toplevel_resumen, text= "-"*60,font=("Arial", 12))
        self.separador1.grid(row=1, column=0,columnspan=2)
        self.lbl_bruto_txt = tk.Label(self.toplevel_resumen, text= "TOTAL BRUTO: ",
                                      font=("Arial", 12))
        self.lbl_bruto_txt.grid(row=2, column=0,sticky="w")
        self.lbl_bruto_val = tk.Label(self.toplevel_resumen, text= f"{total_bruto:.2f}",
                                      font=("Arial", 12))
        self.lbl_bruto_val.grid(row=2, column=1,sticky="e")
        self.lbl_desc_txt = tk.Label(self.toplevel_resumen, text= "TOTAL DESCUENTOS: ",
                                     font=("Arial", 12))
        self.lbl_desc_txt.grid(row=3, column=0,sticky="w")
        self.lbl_desc_val = tk.Label(self.toplevel_resumen, text= f"{total_descuentos:.2f}",
                                     font=("Arial", 12))
        self.lbl_desc_val.grid(row=3, column=1, sticky="e")
        self.lbl_ventas_txt = tk.Label(self.toplevel_resumen, text= "TOTAL VENTAS: ",
                                       font=("Arial", 12))
        self.lbl_ventas_txt.grid(row=4, column=0,sticky="w")
        self.lbl_ventas_val = tk.Label(self.toplevel_resumen, text= f"{total_ventas:.2f}",
                                       font=("Arial", 12))
        self.lbl_ventas_val.grid(row=4, column=1,sticky="e")
        self.lbl_efectivo_txt = tk.Label(self.toplevel_resumen, text= "TOTAL EFECTIVO: ",
                                         font=("Arial", 12))
        self.lbl_efectivo_txt.grid(row=5, column=0,sticky="w")
        self.lbl_efectivo_val = tk.Label(self.toplevel_resumen, text= f"{total_efectivo:.2f}",
                                         font=("Arial", 12))
        self.lbl_efectivo_val.grid(row=5, column=1, sticky="e")
        self.lbl_tarjeta_txt = tk.Label(self.toplevel_resumen, text= "TOTAL TARJETA: ",
                                        font=("Arial", 12))
        self.lbl_tarjeta_txt.grid(row=6, column=0,sticky="w")
        self.lbl_tarjeta_val = tk.Label(self.toplevel_resumen, text= f"{total_tarjeta:.2f}",
                                        font=("Arial", 12))
        self.lbl_tarjeta_val.grid(row=6, column=1, sticky="e")
        self.separador2 = tk.Label(self.toplevel_resumen, text= "-"*60,font=("Arial", 12))
        self.separador2.grid(row=7, column=0,columnspan=2)
        self.lbl_cant_ventas = tk.Label(self.toplevel_resumen, text= "CANTIDAD VENTAS:",
                                        font=("Arial", 12))
        self.lbl_cant_ventas.grid(row=8, column=0,sticky="e")
        self.lbl_tarjeta_val = tk.Label(self.toplevel_resumen, text= f"{cantidad_ventas}",
                                        font=("Arial", 12))
        self.lbl_tarjeta_val.grid(row=8, column=1, sticky="W")

        self.toplevel_resumen.bind("<Return>", lambda x: self.toplevel_resumen.destroy())
        self.toplevel_resumen.bind("<Escape>", lambda x : self.toplevel_resumen.destroy())

    def resumen_vtas(self):
        """genera un resumen de montos para el rango de fechas seleccionado en el registro de ventas"""
        totales= {}
        lista_ventas_resumen = []
        total_ventas= 0
        total_efectivo= 0
        total_tarjeta= 0
        total_bruto= 0
        total_descuentos=0

        for i in self.ventas_selecc:
            if not i["estado"]:
                continue  # se ignora venta anulada
            lista_ventas_resumen.append(i)

        cantidad_ventas = len(lista_ventas_resumen)

        for venta in lista_ventas_resumen:
            total_ventas+= venta["efectivo"] + venta["tarjeta"]
            total_efectivo+= venta["efectivo"]
            total_tarjeta+= venta["tarjeta"]

            for item in venta["articulos"]:
                total_bruto+= item["precio"]*item["cantidad"]
                total_descuentos+= item["cantidad"]*item["precio"]*item["descuento"]/100

        totales={"total_bruto":total_bruto,
                 "total_descuentos":total_descuentos,
                 "total_ventas":total_ventas,
                 "total_efectivo":total_efectivo,
                 "total_tarjeta":total_tarjeta,
                 "cantidad_ventas":cantidad_ventas
                 }

        return totales

    def cambiar_estado_venta(self):
        """cambia el estado de la venta en el registro de ventas
        para que puedan computarse los valores o no en el caso de
        haber aprobado la venta por error o devolucion"""
        try:
            seleccion= self.tabla_archivo.selection()
            if seleccion:
                if messagebox.askyesno(title="CAMBIAR ESTADO",
                                       message = "REALMENTE DESEA CAMBIAR EL ESTADO DE LA VENTA?",
                                       parent= self.toplevel_reg):
                    venta_select = self.tabla_archivo.item(seleccion)["values"][2] # numero de venta

                    with open(r"registro_ventas\\ventas.json", "r+", encoding='utf-8-sig') as file:
                        data = json.load(file)
                        for i, elemento in enumerate(data):
                            if int(elemento["numeracion"])== venta_select:
                                data[i]["estado"] = not data[i]["estado"]
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()

                    ts_inicio,ts_final= self.get_fechas_seleccionadas()
                    self.explorar_archivo_ventas(ts_inicio,ts_final)
                else:
                    pass
            else:
                pass
        except:
            pass

    def normalizar_lista(self):
        """ Normaliza las listas generadas a partir de los archivos
          excel llamando al modulo normalizador que conecta con los 
          distintos modelos de archivos de las distribuidoras"""
        mensaje1= "EL ARCHIVO FUE GENERADO EXITOSAMENTE\n"
        mensaje2= "LOS ARCHIVOS FUERON GENERADOS EXITOSAMENTE"
        mensaje3= "¿DESEA ELIMINAR REGISTROS ANTERIORES?"

        nuevos_archivos = [] # contendrá los nombres de los nuevos archivos normalizados

        if self.modelo_distr_norm.get() == "":
            self.ventana_normalizar.destroy()
        else:
            distribuidora = self.modelo_distr_norm.get()
            lista_archivos = conversor.convertir_a_csv() # devuelve paginas de excel en csv
            if not lista_archivos:
                pass
            else:
                for archivo in lista_archivos:
                    nuevo_archivo = normalizador.normalizar(archivo,distribuidora)
                       
                    if nuevo_archivo == 'error':
                        error = True
                        messagebox.showwarning(title="ERROR!!!",
                                    message = 'NO SE PUDO NORMALIZAR EL ARCHIVO.',
                                    parent= self.ventana_normalizar)
                        break 
                    else:
                        error = False
                        nuevos_archivos.append(nuevo_archivo)

                if not error:
                    messagebox.showinfo(title="INFO",
                                        message = mensaje1 if len(lista_archivos) == 1 else mensaje2,
                                        parent= self.ventana_normalizar)
                    if messagebox.askyesno(title="ELIMINAR REGISTROS",
                                            message = mensaje3,
                                            parent= self.ventana_normalizar
                                            ):
                        self.eliminar_archivos_anteriores(nuevos_archivos,distribuidora)
                    self.btn_salir.focus()

        for archivo in lista_archivos:
            os.remove(archivo)  # borra archivos csv generados en la ubicacion del excel

    def eliminar_archivos_anteriores(self,nuevos_archivos, distribuidora):
        """Elimina archivos generados anteriormente de la misma distribuidora"""
        archivos_anteriores = os.listdir("archivos_normalizados")

        for archivo in archivos_anteriores:
            if archivo not in nuevos_archivos and distribuidora in archivo:
                os.remove(f"archivos_normalizados\\{archivo}")
            else: continue

    def get_fechas_seleccionadas(self):
        "Ajusta el rango horario seleccionado, 00:00hs de fecha inicial hasta 23:59hs de la fecha final"
        ts_inicio= datetime.timestamp(datetime.strptime(self.fecha_inicial.get(),"%d-%m-%Y"))
        ts_final= datetime.timestamp(datetime.strptime(self.fecha_final.get(),"%d-%m-%Y"))+86399
        # le agrego 23hs 59min 59seg (1 dia = 86400seg)
        return ts_inicio,ts_final

    def get_articulo_busq(self):
        return self.articulo_busq.get()

    def get_distribuidoras(self):
        return self.distribuidoras

    def get_distr_selecc(self):
        return self.distr_selecc.get()

    def get_dto_global(self):
        return self.ventas.desc_global_vta


def app():
    ventana = App()
    ventana.root.mainloop()

if __name__ == "__main__":
    app()
