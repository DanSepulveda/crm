import tkinter as tk
from pathlib import Path
from tkinter import ttk


BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR.parent / "assets" / "logo.png"


class VistaInicio(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.app = app

        self.logo = tk.PhotoImage(file=LOGO_PATH).subsample(4)
        ttk.Label(self, image=self.logo, anchor="center").grid(column=1, row=1)

        ttk.Label(
            self,
            text="Sistema de Gestión de Clientes",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(column=1, row=2, pady=20)

        ttk.Label(self, text="Seleccione una opción para continuar").grid(
            column=1, row=3, pady=10
        )

        ttk.Button(
            self,
            text="Gestión de Clientes",
            width=20,
            command=lambda: self.app._mostrar_vista("VistaClientes"),
        ).grid(column=1, row=4, pady=5)

        ttk.Button(
            self,
            text="Ver registro de LOGS",
            width=20,
            command=lambda: self.app._mostrar_vista("VistaLogs"),
        ).grid(column=1, row=5, pady=5)
