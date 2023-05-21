from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter.messagebox import *
import pandas, matplotlib.pyplot as plt
import sqlite3
import re


patron1 = (
    "^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$"
)
patron2 = "^([0-9])*$"
patron3 = "^[0-9]+(\.[0-9]{1,2})?$"


class Vendedores:
    def __init__(self, id, nombre, apellido, tree, tree2, usertype):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.tree = tree
        self.tree2 = tree2
        self.usertype=usertype
        try:
            self.con = sqlite3.connect("empresa.db")
            cursor = self.con.cursor()
            sql = "CREATE TABLE vendedores (id INTEGER PRIMARY KEY NOT NULL UNIQUE, nombre TEXT NOT NULL, apellido TEXT NOT NULL)"
            cursor.execute(sql)
            self.con.commit()
        except:
            self.con = sqlite3.connect("empresa.db")


    def admin_only(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            usertype = self.usertype
            if usertype != 1:
                MessageBox.showinfo("Error", "Requiere permisos de administrador")
                return None
            else:
                return func(*args, **kwargs)

        return wrapper

    @admin_only
    def alta(
        self,
    ):
        if re.match(patron2, self.id):
            if re.match(patron1, self.nombre):
                if re.match(patron1, self.apellido):
                    cursor = self.con.cursor()
                    data = (self.id, self.nombre, self.apellido)
                    sql = "INSERT INTO vendedores(id,nombre,apellido) VALUES (?,?,?)"
                    cursor.execute(sql, data)
                    self.con.commit()
                    MessageBox.showinfo("Validado", "Datos Agregados")
                else:
                    MessageBox.showwarning("Alerta", "Apellido Invalido")
            else:
                MessageBox.showwarning("Alerta", "Nombre Invalido")
        else:
            MessageBox.showwarning("Alerta", "DNI Invalido, solo se permiten números")

    @admin_only
    def modificarvendedor(
        self,
    ):
        cursor = self.con.cursor()
        data = (self.id,)
        sql = "SELECT * FROM vendedores WHERE id = ?;"
        cursor.execute(sql, data)
        rows = cursor.fetchall()
        if rows == []:
            MessageBox.showwarning("Alerta", "DNI Inexistente")
        else:
            messageDelete = askyesno(
                "Modificar Registro", "¿Quiere modificar el registro permanentemente?"
            )
            if messageDelete > 0:
                if re.match(patron1, self.nombre):
                    if re.match(patron1, self.apellido):
                        data = (self.nombre, self.apellido, self.id)
                        sql = "UPDATE vendedores SET nombre = ?, apellido = ? WHERE id = ?;"
                        cursor.execute(sql, data)
                        self.con.commit()
                        showinfo("Confirmado", "Datos Modificados")
                    else:
                        MessageBox.showwarning("Alerta", "Apellido Invalido")
                else:
                    MessageBox.showwarning("Alerta", "Nombre Invalido")
            else:
                showinfo("Anulado", "Datos No Modificados")

    def vervendedor(
        self,
    ):
        Limpieza.limpiartreeview(self.tree)
        cursor = self.con.cursor()
        data = (self.id,)
        sql = "SELECT * FROM vendedores WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()
        rows = cursor.fetchall()
        if rows == []:
            MessageBox.showwarning("Alerta", "DNI Inexistente")
        else:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def verplantilla(
        self,
    ):
        Limpieza.limpiartreeview(self.tree)
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM vendedores")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.con.commit()

    @admin_only
    def borrarvendedor(
        self,
    ):
        item = self.tree.focus()
        valuelist = self.tree.item(item, "values")
        messageDelete = askyesno(
            "Borrar Registro",
            "¿Quiere borrar el vendedor y sus tickets permanentemente?",
        )
        if messageDelete > 0:
            global selectid
            selectid = valuelist[0]
            data = (selectid,)
            print(selectid)
            cursor = self.con.cursor()
            sql = "DELETE FROM vendedores WHERE id = ?"
            cursor.execute(sql, data)
            sql = "DELETE FROM tickets WHERE id = ?"
            cursor.execute(sql, data)
            self.con.commit()
            Limpieza.limpiartreeview(self.tree)
            Limpieza.limpiartreeview(self.tree2)
            showinfo("Confirmado", "Datos Borrados")
            Vendedores.verplantilla(
                self,
            )
        else:
            showinfo("Anulado", "Datos No Borrados")


class Observador:
    def notificar(self, monto):
        if monto > 1000:
            print("El valor registrado es mayor a $1000")


class SujetoTickets:
    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def notificar_observadores(self, monto):
        for observador in self.observadores:
            observador.notificar(monto)


class Tickets:
    def __init__(self, ticket, id2, fecha, total, tree, tree2):
        self.ticket = ticket
        self.id2 = id2
        self.fecha = fecha
        self.total = total
        self.tree = tree
        self.tree2 = tree2

        try:
            self.con = sqlite3.connect("empresa.db")
            cursor = self.con.cursor()
            sql = "CREATE TABLE tickets (ticket TEXT PRIMARY KEY UNIQUE, id TEXT NOT NULL, fecha TEXT NOT NULL, total REAL NOT NULL)"
            cursor.execute(sql)
            self.con.commit()
        except:
            self.con = sqlite3.connect("empresa.db")

        self.sujeto_tickets = SujetoTickets()
        self.observador = Observador()
        self.sujeto_tickets.agregar_observador(self.observador)

    def altaticket(
        self,
    ):
        self.sujeto_tickets = SujetoTickets()
        self.observador = Observador()
        self.sujeto_tickets.agregar_observador(self.observador)
        cursor = self.con.cursor()
        data = (self.id2,)
        sql = "SELECT * FROM vendedores WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()
        rows = cursor.fetchall()
        if rows == []:
            MessageBox.showwarning("Alerta", "DNI Inexistente")
        else:
            if re.match(patron2, self.ticket):
                if re.match(patron3, self.total):
                    cursor = self.con.cursor()
                    data = (
                        self.ticket,
                        self.id2,
                        self.fecha,
                        float(self.total),
                    )
                    sql = "INSERT INTO tickets(ticket,id,fecha,total) VALUES (?,?,?,?)"
                    cursor.execute(sql, data)
                    self.con.commit()
                    monto = float(self.total)
                    self.sujeto_tickets.notificar_observadores(monto)
                    MessageBox.showinfo("Validado", "Ticket Agregado")
                else:
                    MessageBox.showwarning("Alerta", "El Total debe ser numérico")
            else:
                MessageBox.showwarning(
                    "Alerta", "El numero de ticket debe ser numérico"
                )

    def modificarticket(
        self,
    ):
        cursor = self.con.cursor()
        data = (self.ticket,)
        sql = "SELECT * FROM tickets WHERE ticket = ?;"
        cursor.execute(sql, data)
        rows = cursor.fetchall()
        if rows == []:
            MessageBox.showwarning("Alerta", "Ticket Inexistente")
        else:
            messageDelete = askyesno(
                "Modificar Ticket", "¿Quiere modificar el Ticket permanentemente?"
            )
            if messageDelete > 0:
                if re.match(patron3, self.total):
                    data = (self.fecha, self.total, self.ticket)
                    sql = "UPDATE tickets SET fecha = ?, total = ? WHERE ticket = ?;"
                    cursor.execute(sql, data)
                    self.con.commit()
                    if float(self.total) > 1000:
                        self.notificar_observadores()
                    showinfo("Confirmado", "Datos Modificados")
                else:
                    MessageBox.showwarning("Alerta", "El Total debe ser numérico")
            else:
                showinfo("Anulado", "Datos No Modificados")

    def vertotalvendedor(
        self,
    ):
        Limpieza.limpiartreeview(self.tree2)
        cursor = self.con.cursor()
        data = (self.id2,)
        sql = "SELECT ticket, id, fecha,total FROM tickets WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()
        rows = cursor.fetchall()
        if rows == []:
            MessageBox.showwarning("Alerta", "DNI Inexistente")
        else:
            for row in rows:
                print(row)
                self.tree2.insert("", "end", values=row)

    def borrarticket(
        self,
    ):
        item = self.tree2.focus()
        valuelist = self.tree2.item(item, "values")
        messageDelete = askyesno(
            "Borrar Ticket", "¿Quiere borrar el Ticket permanentemente?"
        )
        if messageDelete > 0:
            global selectticket
            selectticket = valuelist[0]
            id2 = valuelist[1]
            print(id2)
            data = (selectticket,)
            cursor = self.con.cursor()
            sql = "DELETE FROM tickets WHERE ticket = ?"
            cursor.execute(sql, data)
            self.con.commit()
            self.tree2.delete(item)
            showinfo("Confirmado", "Ticket Borrado")
            Tickets.vertotalvendedor(
                self,
            )
        else:
            showinfo("Anulado", "Ticket No Borrado")


class Helper:
    def __init__(self, tree, tree2):
        self.tree = tree
        self.tree2 = tree2
        self.con = sqlite3.connect("empresa.db")

    def graficar(
        self,
    ):
        sql = "select t.id, sum(t.total) as sum_gastos, v.nombre, v.apellido FROM tickets t, vendedores v where t.id = v.id GROUP BY t.id, v.nombre, v.apellido"
        data = pandas.read_sql(sql, self.con)
        x = data.id + "\n" + data.nombre + " " + data.apellido
        plt.bar(x, data.sum_gastos, label="Total de Gastos")
        plt.legend()
        plt.title("Total de Gastos por Vendedor")
        plt.show()

    def clickviews(self, tree, tree2):
        item = tree.focus()
        valuelist = tree.item(item, "values")
        selectid = valuelist[0]
        data = (selectid,)
        cursor = self.con.cursor()
        sql = "SELECT ticket, id, fecha,total FROM tickets WHERE id = ?;"
        cursor.execute(sql, data)
        self.con.commit()
        Limpieza.limpiartreeview(tree2)
        rows = cursor.fetchall()
        for row in rows:
            tree2.insert("", "end", values=row)


class Limpieza:
    def limpiartreeview(arbol):
        for item in arbol.get_children():
            arbol.delete(item)
