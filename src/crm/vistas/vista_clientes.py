from tkinter import ttk


class VistaClientes(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app

        ttk.Button(
            self,
            text="volver",
            command=lambda: self.app._mostrar_vista("VistaInicio"),
        ).pack()

        ttk.Label(self, text="Tabla de Clientes").pack()
