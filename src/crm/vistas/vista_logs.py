from tkinter import ttk


class VistaLogs(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app

        ttk.Button(
            self,
            text="volver",
            command=lambda: self.app.mostrar_vista("VistaInicio"),
        ).pack()

        ttk.Label(self, text="Tabla de logs").pack()
