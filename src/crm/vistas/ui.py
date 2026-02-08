from tkinter import ttk


class UI:
    @staticmethod
    def campo(frame, label, columna, fila, mb: bool = False):
        cframe = ttk.Frame(frame)
        cframe.grid(column=columna, row=fila)

        label_campo = ttk.Label(cframe, text=label, font=("Arial", 14, "bold"))
        label_campo.grid(column=0, row=0, padx=5, sticky="w")

        entry = ttk.Entry(cframe, width=25)
        entry.grid(column=0, row=1, padx=5, pady=(0, 20) if mb else 0)
        return entry

    @staticmethod
    def combo(
        frame, label, columna, fila, valores, mb: bool = False, **kwargs
    ):
        cframe = ttk.Frame(frame)
        cframe.grid(column=columna, row=fila)

        label_campo = ttk.Label(cframe, text=label, font=("Arial", 14, "bold"))
        label_campo.grid(column=0, row=0, padx=5, sticky="w")

        state = "readonly"
        entry = ttk.Combobox(
            cframe, values=valores, state=state, width=23, **kwargs
        )
        entry.grid(column=0, row=1, padx=5, pady=(0, 20) if mb else 0)
        return entry

    @staticmethod
    def _separador(frame, row):
        ttk.Separator(frame, orient="horizontal").grid(
            column=0, row=row, pady=10
        )
