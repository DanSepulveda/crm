import tkinter as tk
from pathlib import Path
from tkinter import ttk


BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR.parent / "assets" / "logo.png"


class VistaInicio(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app

        self.logo = tk.PhotoImage(file=LOGO_PATH).subsample(3)
        ttk.Label(self, image=self.logo, anchor="center").pack()
        ttk.Label(self, text="Selecciona una opción para comenzar").pack()

        ttk.Button(
            self,
            text="Gestión de Clientes",
            command=lambda: self.app._mostrar_vista("VistaClientes"),
        ).pack()

        ttk.Button(
            self,
            text="Ver registro de LOGS",
            command=lambda: self.app._mostrar_vista("VistaLogs"),
        ).pack()
