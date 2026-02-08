import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import TYPE_CHECKING


# Se importa App solo en desarrollo para poder usar su tipo. En tiempo de
# ejecución se ignora el import ya que genera dependencia circular
if TYPE_CHECKING:
    from src.crm.app import App


BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR.parent / "assets" / "logo.png"


class VistaInicio(ttk.Frame):
    def __init__(self, padre, app: "App"):
        super().__init__(padre)
        self._app = app
        self._logo = tk.PhotoImage(file=LOGO_PATH).subsample(4)

        # Configuración de columnas y filas "fantasmas" para centrar contenido
        self.rowconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        # ----------------------- Elementos de la vista -----------------------
        imagen = ttk.Label(self, image=self._logo, anchor="center")
        imagen.grid(column=1, row=1)

        ttk.Label(
            self,
            text="Sistema de Gestión de Clientes",
            font=("TkDefaultFont", 16, "bold"),
        ).grid(column=1, row=2, pady=20)

        sub = ttk.Label(self, text="Seleccione una opción para continuar")
        sub.grid(column=1, row=3, pady=10)

        ttk.Button(
            self,
            text="Gestión de Clientes",
            width=20,
            command=lambda: self._app._mostrar_vista("VistaClientes"),
        ).grid(column=1, row=4, pady=5)

        ttk.Button(
            self,
            text="Ver registro de LOGS",
            width=20,
            command=lambda: self._app._mostrar_vista("VistaLogs"),
        ).grid(column=1, row=5, pady=5)
