import tkinter as tk
from tkinter import ttk

from src.crm.cliente import ServicioCliente
from src.crm.vistas import (
    VistaClientes,
    VistaFormulario,
    VistaInicio,
    VistaLogs,
)


class App(tk.Tk):
    def __init__(self, servicio_cliente: ServicioCliente):
        super().__init__()
        self.rut_usuario_seleccionado = None
        self._servicio_cliente = servicio_cliente
        self._vistas = {}

        # CONFIGURACIÓN VENTANA
        self.title("Gestión de clientes")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.config(padx=30, pady=30)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ESTILOS TKINTER
        style = ttk.Style()

        style.configure(
            "Custom.TButton", foreground="white", background="blue"
        )
        style.configure("Treeview", rowheight=30)

        style.map(
            "Custom.TButton",
            foreground=[("disabled", "gray")],
            background=[("disabled", "#d9d9d9")],
        )

        for vista in (VistaClientes, VistaFormulario, VistaInicio, VistaLogs):
            frame = vista(self, self)
            self._vistas[vista.__name__] = frame
            frame.grid(column=0, row=0, sticky="nsew")

        self._mostrar_vista("VistaInicio")

    @property
    def rut_usuario_seleccionado(self) -> str | None:
        return self._rut_usuario_seleccionado

    @rut_usuario_seleccionado.setter
    def rut_usuario_seleccionado(self, rut: str | None):
        self._rut_usuario_seleccionado = rut

    def _mostrar_vista(self, nombre_vista: str):
        vista = self._vistas[nombre_vista]
        if not vista:
            raise ValueError(f"Vista '{nombre_vista}' no existe.")
        vista.tkraise()

        if hasattr(vista, "resetear"):
            vista.resetear()

    def mostrar_formulario_creacion(self):
        form = self._vistas["VistaFormulario"]
        form.preparar_creacion()
        form.tkraise()

    def mostrar_formulario_edicion(self):
        pass
