"""
Ël módulo controlador.py contiene la clase controller
con la que se lanza el programa"""
from tkinter import *
from tkinter import Tk
from tkinter import ttk
import vista


class Controller:
    def __init__(self):
        """
        instancia la clase Ventana del módulo vista para poder lanzar el programa

        root = Tk()
        start = vista.Ventana(root)
        root.mainloop()
        """

        root = Tk()
        start = vista.Login(root)    
        root.mainloop()

"""Dispara el programa"""
load = Controller()
