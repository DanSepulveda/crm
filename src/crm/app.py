import tkinter as tk
from tkinter import ttk

from src.crm.cliente import ServicioCliente
from src.crm.vistas import VistaClientes, VistaInicio, VistaLogs


class App(tk.Tk):
    def __init__(self, servicio_cliente: ServicioCliente):
        super().__init__()
        self.servicio_cliente = servicio_cliente

        # CONFIGURACIÓN VENTANA
        self.title("Gestión de clientes")
        self.geometry("900x500")
        self.minsize(1000, 400)
        self.config(padx=20, pady=20)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # DICCIONARIO DONDE SE ALMACENAN TODAS LAS VISTAS
        self._vistas = {}

        # CONTENEDOR PRINCIPAL DE LAS VISTAS
        container = ttk.Frame(self)
        container.grid(column=0, row=0)

        for vista in (VistaClientes, VistaInicio, VistaLogs):
            frame = vista(container, self)
            self._vistas[vista.__name__] = frame
            frame.grid(column=0, row=0, sticky="nsew")

        self._mostrar_vista("VistaInicio")

    def _mostrar_vista(self, nombre_vista: str):
        frame = self._vistas[nombre_vista]
        frame.tkraise()
