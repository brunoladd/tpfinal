from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter import ttk
from tkinter import Tk
from tkcalendar import DateEntry
from datetime import date
import tkinter as tk
import modelo

class Login:
    def __init__(self,login):
    # Crear la ventana principal
        self.login = login
        login.title("Login")

        # Definir el tamaño deseado
        ancho = 320
        alto = 100

        # Establecer el tamaño de la ventana
        login.geometry(f"{ancho}x{alto}")    

        var_usuario = StringVar()
        var_contrasenia = StringVar()

        usuario_label = Label(login, text="Usuario")
        usuario_label.grid(row=3, column=0, sticky=E)
        contrasenia_label = Label(login, text="Contraseña")
        contrasenia_label.grid(row=4, column=0, sticky=E)

        usuario_entry = Entry(login, textvariable=var_usuario)
        usuario_entry.grid(row=3, column=1)
        contrasenia_entry = Entry(login, textvariable=var_contrasenia)
        contrasenia_entry.config(show="*")
        contrasenia_entry.grid(row=4, column=1)

        def abrir_ventana_secundaria(self,usertype):
            main = Tk()
            ventana_secundaria = Ventana(main,usertype)
            ventana_secundaria.transient(self)  # Hace que la ventana secundaria sea dependiente de la ventana principal
            ventana_secundaria.grab_set()  # Bloquea la interacción con la ventana principal mientras la secundaria esté abierta
            ventana_secundaria.focus_set()  # Da el foco a la ventana secundaria

        boton_login = Button(
            login,
            text="Iniciar Sesión",
            command=lambda: verificar_credenciales(),
        )
        boton_login.grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E)

        def verificar_credenciales():
            # Función para verificar las credenciales de inicio de sesión
            usuario = var_usuario.get()
            contraseña = var_contrasenia.get()

            if usuario == "admin" and contraseña == "12345":
                # Cerrar la ventana de inicio de sesión
                login.destroy()
                # Llamar a la función para abrir la nueva ventana como un usuario administrador
                abrir_ventana_secundaria(self,1)
            else:
                login.destroy()
                # Llamar a la función para abrir la nueva ventana como un usuario comun
                abrir_ventana_secundaria(self,0)
                print("Credenciales inválidas")

class Ventana:
    def __init__(self,master,usertype):
        self.master = master
        self.usertype = usertype
        master.title("ABM  Vendedores y Tickets")

        var_nombre = StringVar()
        var_apellido = StringVar()
        var_id = StringVar()
        var_id2 = StringVar()
        var_ticket = StringVar()
        var_fecha = StringVar()
        var_total = StringVar()

        label = Label(master, text="ABM Vendores", bg="sky blue", width="50")
        label.grid(row=0, column=0, columnspan=3)

        label = Label(master, text="ABM Tickets", bg="skyblue3", width="50")
        label.grid(row=0, column=3, columnspan=3)

        # abm vendedores

        id_label = Label(master, text="DNI")
        id_label.grid(row=1, column=0, sticky=E)
        nombre_label = Label(master, text="Nombre")
        nombre_label.grid(row=2, column=0, sticky=E)
        apellido_label = Label(master, text="Apellido")
        apellido_label.grid(row=3, column=0, sticky=E)

        id_entry = Entry(master, textvariable=var_id)
        id_entry.grid(row=1, column=1)
        nombre_entry = Entry(master, textvariable=var_nombre)
        nombre_entry.grid(row=2, column=1)
        apellido_entry = Entry(master, textvariable=var_apellido)
        apellido_entry.grid(row=3, column=1)

        boton_av = Button(
            master,
            text="Cargar Nuevo ID",
            command=lambda: llamaralta(),
        )
        boton_av.grid(row=1, column=2, sticky=E)

        def llamaralta():
            mivendedor = modelo.Vendedores(
                var_id.get(), var_nombre.get(), var_apellido.get(), None, None, self.usertype
            )
            mivendedor.alta()

        boton_mv = Button(
            master,
            text="Modificar ID",
            command=lambda: llamarmodificar(),
        )
        boton_mv.grid(row=2, column=2, sticky=E)

        def llamarmodificar():
            mivendedor = modelo.Vendedores(
                var_id.get(), var_nombre.get(), var_apellido.get(), None, None, self.usertype
            )
            mivendedor.modificarvendedor()

        boton_bv = Button(
            master,
            text="Borrar ID",
            command=lambda: llamarborrar(),
        )
        boton_bv.grid(row=3, column=2, sticky=E)

        def llamarborrar():
            mivendedor = modelo.Vendedores(None, None, None, tree, tree2, self.usertype)
            mivendedor.borrarvendedor()

        boton_vv = Button(
            master,
            text="Mostrar Vendedor",
            command=lambda: llamarmostrar(),
        )

        boton_vv.grid(row=4, column=2, sticky=E)

        def llamarmostrar():
            mivendedor = modelo.Vendedores(var_id.get(), None, None, tree, None, None)
            mivendedor.vervendedor()

        boton_vp = Button(
            master,
            text="Ver toda la Plantilla",
            command=lambda: llamarplantilla(),
        )
        boton_vp.grid(row=5, column=2, sticky=E)

        def llamarplantilla():
            mivendedor = modelo.Vendedores(None, None, None, tree, None, None)
            mivendedor.verplantilla()

        # abm tickets

        id2_label = Label(master, text="DNI")
        id2_label.grid(row=1, column=3, sticky=E)
        ticket = Label(master, text="Nro de Ticket")
        ticket.grid(row=2, column=3, sticky=E)
        fecha = Label(master, text="Fecha")
        fecha.grid(row=3, column=3, sticky=E)
        total = Label(master, text="Total en $")
        total.grid(row=4, column=3, sticky=E)

        id2_entry = Entry(master, textvariable=var_id2)
        id2_entry.grid(row=1, column=4)
        ticket = Entry(master, textvariable=var_ticket)
        ticket.grid(row=2, column=4)
        fecha = DateEntry(
            master,
            width=18,
            background="darkblue",
            foreground="black",
            borderwidth=2,
            textvariable=var_fecha,
            selectmode='day',
        )
        fecha.grid(row=3, column=4)
        total = Entry(master, textvariable=var_total)
        total.insert(0, "0.00")
        total.grid(row=4, column=4)

        boton_av = Button(
            master,
            text="Cargar Nuevo Ticket",
            command=lambda: llamarticket(),
        )
        boton_av.grid(row=1, column=5, sticky=E)

        def llamarticket():
            miticket = modelo.Tickets(
                var_ticket.get(),
                var_id2.get(),
                var_fecha.get(),
                var_total.get(),
                None,
                None,
            )
            miticket.altaticket()

        boton_mv = Button(
            master,
            text="Borrar Ticket",
            command=lambda: llamarborrarticket(),
        )
        boton_mv.grid(row=2, column=5, sticky=E)

        def llamarborrarticket():
            miticket = modelo.Tickets(None, None, None, None, None, tree2)
            miticket.borrarticket()

        boton_bv = Button(
            master,
            text="Modificar Ticket",
            command=lambda: llamarmodificarticket(),
        )
        boton_bv.grid(row=3, column=5, sticky=E)

        def llamarmodificarticket():
            miticket = modelo.Tickets(
                var_ticket.get(), None, var_fecha.get(), var_total.get(), None, None
            )
            miticket.modificarticket()

        boton_vv = Button(
            master,
            text="Ver Total Vendedor",
            command=lambda: llamarvertotalvendedor(),
        )

        boton_vv.grid(row=4, column=5, sticky=E)

        def llamarvertotalvendedor():
            miticket = modelo.Tickets(None, var_id2.get(), None, None, None, tree2)
            miticket.vertotalvendedor()

        boton_gv = Button(
            master,
            text="Graficar Total Vendedor",
            command=lambda: llamargraficar(),
        )
        boton_gv.grid(row=5, column=5, sticky=E)

        def llamargraficar():
            mihelper = modelo.Helper(None, None)
            mihelper.graficar()

        # definimos el treeview de vendedores

        tree2 = ttk.Treeview(master)
        columns2 = ("ticket", "id", "fecha", "total")
        tree2 = ttk.Treeview(master, columns=columns2, show="headings")
        tree2.column("ticket", width=60, minwidth=50)
        tree2.heading("ticket", text="Nro. Ticket")
        tree2.column("id", width=90, minwidth=50)
        tree2.heading("id", text="DNI")
        tree2.column("fecha", width=150, minwidth=80)
        tree2.heading("fecha", text="Fecha")
        tree2.column("total", width=150, minwidth=80)
        tree2.heading("total", text="Total en $")
        tree2.bind('<<TreeviewSelect>>', lambda event: selecttree2(binding='TreeviewSelect'))
        tree2.grid(column=3, row=6, columnspan=4, sticky=W)

        tree = ttk.Treeview(master)
        columns = ("id", "nombre", "apellido")
        tree = ttk.Treeview(master, columns=columns, show="headings")
        tree.column("id", width=80, minwidth=50)
        tree.heading("id", text="DNI")
        tree.column("nombre", width=185, minwidth=50)
        tree.heading("nombre", text="Nombre")
        tree.column("apellido", width=185, minwidth=50)
        tree.heading("apellido", text="Apellido")
        tree.bind('<<TreeviewSelect>>', lambda event: clickviews(binding='TreeviewSelect'))
        tree.grid(column=0, row=6, columnspan=4, sticky=W)

        def clickviews(binding):
            mihelper = modelo.Helper(tree, tree2)
            mihelper.clickviews(tree, tree2)
            var_id2.set("")
            var_ticket.set("")
            var_fecha.set(date.today())
            var_total.set("")

        def selecttree2(binding):
            item = tree2.focus()
            valuelist = tree2.item(item, "values")
            try:
                selectid = valuelist[1]
                selectticket = valuelist[0]
                selectfecha = valuelist[2]
                selecttotal = valuelist[3]            
                var_id2.set(selectid)
                var_ticket.set(selectticket)
                var_fecha.set(selectfecha)
                var_total.set(selecttotal)
            except:
                print("aun no se selecciona nintun registro en el tree de ticket")
    
        

