import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from src.crm.cliente import ServicioCliente
from src.crm.vistas import (
    VistaClientes,
    VistaFormulario,
    VistaInicio,
    VistaLogs,
)


if TYPE_CHECKING:
    from src.crm.cliente import (
        ClienteCorporativo,
        ClientePremium,
        ClienteRegular,
    )


class App(tk.Tk):
    def __init__(self, servicio_cliente: ServicioCliente):
        super().__init__()
        self.cliente_seleccionado: (
            ClienteCorporativo | ClienteRegular | ClientePremium | None
        ) = None
        self.servicio_cliente = servicio_cliente
        self._vistas = {}

        # CONFIGURACIÓN VENTANA
        self.title("Gestión de clientes")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.config(padx=30, pady=30)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # ESTILOS TKINTER
        self.configure(bg="#f3f3f3")
        self.option_add("*TCombobox*Listbox.font", "SegoeUI 11")
        self.option_add("*TCombobox*Listbox.background", "white")
        self.option_add("*TCombobox*Listbox.foreground", "#363636")
        self.option_add("*TCombobox*Listbox.selectBackground", "#0078d7")
        self.option_add("*TCombobox*Listbox.selectForeground", "white")
        self.option_add("*TCombobox*Listbox.relief", "flat")
        self.option_add("*TCombobox*Listbox.borderwidth", 5)

        style = ttk.Style()
        style.theme_use("clam")

        # button
        style.configure(
            "Primary.TButton",
            padding=(2, 7, 2, 7),
            foreground="white",
            background="#0067c0",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#00529a")],
            foreground=[("active", "white")],
        )
        style.configure(
            "Secondary.TButton",
            padding=(0, 5, 0, 5),
            foreground="#0067c0",
            background="#f3f3f3",
            font=("Segoe UI Semibold", 10),
            borderwidth=1,
            bordercolor="#0067c0",
        )
        style.map(
            "Secondary.TButton",
            foreground=[("active", "#003f76"), ("disabled", "#a0a0a0")],
            background=[("active", "#e3f2ff")],
            bordercolor=[("disabled", "#d1d1d1")],
        )
        style.configure(
            "Danger.TButton",
            padding=(0, 5, 0, 5),
            foreground="#c42b1c",
            background="#f3f3f3",
            font=("Segoe UI Semibold", 10),
            borderwidth=1,
            bordercolor="#c42b1c",
        )
        style.map(
            "Danger.TButton",
            foreground=[("active", "#7e1b12"), ("disabled", "#a0a0a0")],
            background=[("active", "#ffe3e1")],
            bordercolor=[("disabled", "#d1d1d1")],
        )
        # label
        style.configure("TLabel", background="#f3f3f3", foreground="#1a1a1a")
        style.configure("Entry.TLabel", font=("Segoe UI Semibold", 10, "bold"))
        style.configure("Titulo.TLabel", font=("Segoe UI", 12, "bold"))
        # entry y combobox
        style.configure(
            "TEntry",
            fieldbackground="white",
            foreground="#363636",
            padding=5,
            borderwidth=2,
            font=("Segoe UI", 11),
        )
        style.map(
            "TEntry",
            fieldbackground=[("selected", "white"), ("disabled", "#f3f3f3")],
            bordercolor=[("focus", "#0078d7")],
        )
        style.configure(
            "TCombobox",
            fieldbackground="white",
            foreground="#1a1a1a",
            padding=5,
            borderwidth=2,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "white"), ("disabled", "#f3f3f3")],
            selectbackground=[("focus", "white"), ("!focus", "white")],
            selectforeground=[("focus", "#1a1a1a"), ("!focus", "#1a1a1a")],
            bordercolor=[("focus", "#0078d7")],
        )
        # frame
        style.configure("TFrame", background="#f3f3f3")
        # treeview
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#1a1a1a",
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", "#cfeaff")],
            foreground=[("selected", "#1a1a1a")],
        )
        style.configure(
            "Treeview.Heading",
            background="#f3f3f3",
            foreground="#1a1a1a",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview.Heading", background=[("active", "#e5e5e5")])
        # scrollbar
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#cccccc",
            darkcolor="#cccccc",
            lightcolor="#cccccc",
            troughcolor="#f3f3f3",
            bordercolor="#f3f3f3",
            arrowsize=12,
        )
        style.map(
            "Vertical.TScrollbar",
            background=[("active", "#aaaaaa"), ("pressed", "#888888")],
        )

        for vista in (VistaClientes, VistaFormulario, VistaInicio, VistaLogs):
            frame = vista(self, self)
            self._vistas[vista.__name__] = frame
            frame.grid(column=0, row=0, sticky="nsew")

        self.mostrar_vista("VistaInicio")

    def mostrar_vista(self, nombre_vista: str):
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
        form = self._vistas["VistaFormulario"]
        form.preparar_edicion()
        form.tkraise()
