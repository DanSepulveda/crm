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
        self._logo = tk.PhotoImage(file=LOGO_PATH)

        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True)

        # ----------------------- Elementos de la vista -----------------------
        ttk.Label(contenedor, image=self._logo).pack()

        ttk.Label(
            contenedor,
            text="Sistema de Gestión de Clientes",
            font=("TkDefaultFont", 16, "bold"),
        ).pack(pady=20)

        ttk.Label(
            contenedor, text="Seleccione una opción para continuar"
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Gestión de Clientes",
            width=20,
            command=lambda: self._app._mostrar_vista("VistaClientes"),
        ).pack(pady=5)

        ttk.Button(
            contenedor,
            text="Ver registro de LOGS",
            width=20,
            command=lambda: self._app._mostrar_vista("VistaLogs"),
        ).pack(pady=5)
