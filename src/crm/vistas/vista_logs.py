from datetime import datetime
from tkinter import ttk
from typing import TYPE_CHECKING, Literal

from src.crm.utilidades import Logger


# Se importa App solo en desarrollo para poder usar su tipo. En tiempo de
# ejecución se ignora el import ya que genera dependencia circular
if TYPE_CHECKING:
    from src.crm.app import App


class VistaLogs(ttk.Frame):
    def __init__(self, padre, app: "App"):
        super().__init__(padre)
        self._app = app

        # Configuración de filas y columnas
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # ---------------------- FRAME LOGS (IZQUIERDA) -----------------------
        frame_logs = ttk.Frame(self)
        frame_logs.grid(column=0, row=0, padx=(0, 20), sticky="nsew")

        # label para mostrar cantidad de logs
        self._titulo = ttk.Label(frame_logs, style="Titulo.TLabel")
        self._titulo.pack(pady=(0, 15))

        # 3 -> frame para tabla y scroll
        frame_tabla = ttk.Frame(frame_logs)
        frame_tabla.pack(side="top", fill="both", expand=True)

        # - scrollbar
        scroll_y = ttk.Scrollbar(frame_tabla)
        scroll_y.pack(side="right", fill="y")

        # - tabla
        columnas: list[tuple[str, int, Literal["e", "w", "center"]]] = [
            ("N°", 40, "e"),
            ("Fecha", 110, "e"),
            ("Hora", 90, "e"),
            ("Tipo", 100, "center"),
            ("Descripción", 200, "w"),
        ]
        self._tabla = ttk.Treeview(
            frame_tabla,
            columns=[c[0] for c in columnas],
            show="headings",
            yscrollcommand=scroll_y.set,
        )
        self._tabla.pack(side="left", fill="both", expand=True)
        self._tabla.tag_configure("ERROR", foreground="#B22525")
        self._tabla.tag_configure("WARNING", foreground="#a16a1e")
        self._tabla.tag_configure('fila_impar', background='#ffffff')
        self._tabla.tag_configure('fila_par', background='#f9f9f9')
        scroll_y.config(command=self._tabla.yview)

        # - agregar encabezados y configurar columnas
        for columna in columnas:
            nombre, ancho, posicion = columna
            self._tabla.column(
                nombre,
                width=ancho,
                minwidth=ancho,
                anchor=posicion,
                stretch=nombre == "Descripción",
            )
            self._tabla.heading(nombre, text=nombre, anchor=posicion)

        # -------------------- FRAME BOTONES (DERECHA) ------------------------
        frame_opciones = ttk.Frame(self)
        frame_opciones.grid(column=1, row=0, sticky="n")

        ttk.Button(
            frame_opciones,
            text="Volver al inicio",
            width=22,
            style="Secondary.TButton",
            command=lambda: self._app.mostrar_vista("VistaInicio"),
        ).pack()

    def resetear(self):
        self._refrescar_tabla()

    def _refrescar_tabla(self):
        """Rellena la tabla con los logs del sistema."""
        self._tabla.delete(*self._tabla.get_children())  # limpia la tabla

        logs = Logger.leer_ultimos_logs()
        if not logs:
            titulo = "No hay logs almacenados."
        else:
            titulo = f"Mostrando {len(logs)} últimos registros."

            for i, log in enumerate(logs, 1):
                fecha_log, tipo, descripcion = log

                dt = datetime.strptime(fecha_log, "%Y-%m-%d %H:%M:%S,%f")
                fecha = dt.date().strftime("%d-%m-%Y")
                hora = dt.time().replace(microsecond=0)
                self._tabla.insert(
                    "",
                    "end",
                    values=(
                        str(i),
                        str(fecha),
                        str(hora),
                        tipo.replace("ING", ""),
                        descripcion,
                    ),
                    tags=(tipo, 'fila_par' if i % 2 == 0 else 'fila_impar'),
                )
        self._titulo.config(text=titulo)
