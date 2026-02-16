import tkinter as tk
from tkinter import ttk


class ComponentesTkinter:
    @staticmethod
    def campo(
        frame,
        label,
        columna,
        fila,
        mb: bool = False,
        width: int = 40,
        **kwargs,
    ):
        cframe = ttk.Frame(frame)
        cframe.grid(column=columna, row=fila)

        label_campo = ttk.Label(cframe, text=label, style="Entry.TLabel")
        label_campo.grid(column=0, row=0, padx=10, sticky="w")

        entry = ttk.Entry(cframe, width=width, **kwargs)
        entry.grid(column=0, row=1, padx=10, pady=(0, 15) if mb else 0)
        return entry

    @staticmethod
    def combo(
        frame, label, columna, fila, valores, mb: bool = False, **kwargs
    ):
        cframe = ttk.Frame(frame)
        cframe.grid(column=columna, row=fila)

        label_campo = ttk.Label(cframe, text=label, style="Entry.TLabel")
        label_campo.grid(column=0, row=0, padx=10, sticky="w")

        state = "readonly"
        entry = ttk.Combobox(
            cframe, values=valores, state=state, width=38, height=8, **kwargs
        )
        entry.grid(column=0, row=1, padx=10, pady=(0, 15) if mb else 0)
        return entry

    @staticmethod
    def separador_horizontal(frame):
        linea = tk.Frame(frame, bg="#d1d1d1", height=1)
        linea.pack(fill="x", padx=10, pady=20)
