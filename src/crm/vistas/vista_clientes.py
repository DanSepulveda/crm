import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Literal


# Se importa App solo en desarrollo para poder usar su tipo. En tiempo de
# ejecución se ignora el import ya que genera dependencia circular
if TYPE_CHECKING:
    from src.crm.app import App


class VistaClientes(ttk.Frame):
    def __init__(self, padre, app: "App"):
        super().__init__(padre)
        self._app = app

        # Configuración de filas y columnas
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # -------------------- FRAME CLIENTES (IZQUIERDA) ---------------------
        frame_clientes = ttk.Frame(self)
        frame_clientes.grid(column=0, row=0, padx=(0, 20), sticky="nsew")

        # 1 -> frame busqueda
        frame_busqueda = ttk.Frame(frame_clientes)
        frame_busqueda.pack(side="top", fill="x")

        ttk.Label(frame_busqueda, text="Búsqueda").pack(side="left")

        self._buscador = ttk.Entry(frame_busqueda)
        self._buscador.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # 2 -> label para mostrar resultado de búsqueda
        self._titulo = ttk.Label(frame_clientes, font="Arial 14 bold")
        self._titulo.pack(pady=15)

        # 3 -> frame para tabla y scroll
        frame_tabla = ttk.Frame(frame_clientes)
        frame_tabla.pack(side="top", fill="both", expand=True)

        # - scrollbar
        scroll_y = ttk.Scrollbar(frame_tabla)
        scroll_y.pack(side="right", fill="y")

        # - tabla
        columnas: list[tuple[str, int, Literal["e", "w", "center"]]] = [
            ("N°", 40, "e"),
            ("Tipo", 80, "center"),
            ("RUT", 120, "e"),
            ("Nombres", 150, "w"),
            ("Apellido paterno", 150, "w"),
            ("Apellido materno", 150, "w"),
        ]
        self._tabla = ttk.Treeview(
            frame_tabla,
            columns=[c[0] for c in columnas],
            show="headings",
            yscrollcommand=scroll_y.set,
        )
        self._tabla.pack(side="left", fill="both", expand=True)
        scroll_y.config(command=self._tabla.yview)

        # - agregar encabezados y configurar columnas
        for columna in columnas:
            nombre, ancho, posicion = columna
            self._tabla.column(
                nombre,
                width=ancho,
                minwidth=ancho,
                anchor=posicion,
                stretch=nombre == "Nombres",
            )
            self._tabla.heading(nombre, text=nombre)

        self._buscador.bind("<KeyRelease>", self._onchange_busqueda)
        self._tabla.bind("<<TreeviewSelect>>", self._onclick_fila)
        self._refrescar_tabla()

        # -------------------- FRAME BOTONES (DERECHA) ------------------------
        frame_opciones = ttk.Frame(self)
        frame_opciones.grid(column=1, row=0, sticky="n")

        ttk.Button(
            frame_opciones,
            text="Crear Usuario",
            width=15,
            command=self._app.mostrar_formulario_creacion,
        ).pack(pady=(0, 10))

        self._btn_editar = ttk.Button(
            frame_opciones,
            text="Editar usuario",
            width=15,
            state="disabled",
            style="Custom.TButton",
            command=self._app.mostrar_formulario_edicion,
        )
        self._btn_editar.pack(pady=(0, 10))

        self._btn_eliminar = ttk.Button(
            frame_opciones,
            text="Eliminar usuario",
            width=15,
            state="disabled",
            style="Custom.TButton",
            command=self._onclick_eliminar,
        )
        self._btn_eliminar.pack(pady=(0, 10))

        ttk.Button(
            frame_opciones,
            text="Volver al inicio",
            width=15,
            command=lambda: self._app.mostrar_vista("VistaInicio"),
        ).pack(pady=(40, 0))

    def resetear(self):
        self._buscador.delete(0, tk.END)
        self._refrescar_tabla()

    def _refrescar_tabla(self, busqueda: str = ""):
        """Rellena la tabla con los clientes resultantes de la búsqueda."""
        self._tabla.delete(*self._tabla.get_children())  # limpia la tabla

        clientes = self._app.servicio_cliente.obtener_todos()
        filtrados = self._app.servicio_cliente.obtener_filtrados(busqueda)

        if not clientes:
            titulo = "No hay clientes registrados."
        elif not filtrados:
            titulo = "Sin resultados para la búsqueda."
        else:
            titulo = f"Mostrando {len(filtrados)} de {len(clientes)} clientes."

            # se rellena la tabla con los clientes filtrados
            for i, c in enumerate(filtrados, 1):
                self._tabla.insert(
                    "",
                    "end",
                    values=(
                        str(i),
                        c.TIPO,
                        c.rut + " " * 3,
                        " " * 3 + c.nombres,
                        " " * 3 + c.apellido_paterno,
                        " " * 3 + c.apellido_materno,
                    ),
                )
        self._titulo.config(text=titulo)

    def _onchange_busqueda(self, _):
        """Refresca la tabla cada vez que se escribe en el buscador."""
        busqueda = self._buscador.get()
        self._refrescar_tabla(busqueda)

    def _onclick_fila(self, _):
        """Activa/desactiva botones dependiendo si hay una fila seleccionada."""
        seleccion = self._tabla.selection()

        if seleccion:
            id_item = seleccion[0]
            rut_elegido: str = self._tabla.item(id_item, "values")[2].strip()
            self._app.cliente_seleccionado = (
                self._app.servicio_cliente.obtener_uno(rut_elegido)
            )
            estado = "normal"
        else:
            self._app.cliente_seleccionado = None
            estado = "disabled"

        self._btn_editar.config(state=estado)
        self._btn_eliminar.config(state=estado)

    def _onclick_eliminar(self):
        """Ejecuta el servicio de eliminación, previa confirmación."""
        cliente = self._app.cliente_seleccionado
        if cliente is None:
            return

        confirmar = messagebox.askokcancel(
            "Confirmar eliminación",
            "¿Seguro que desea eliminar al cliente seleccionado?",
        )
        if confirmar:
            res = self._app.servicio_cliente.eliminar_cliente(cliente.rut)
            if res.exito:
                busqueda = self._buscador.get()
                self._refrescar_tabla(busqueda)
                messagebox.showinfo("OK", res.mensaje)
            else:
                messagebox.showerror("Error", res.mensaje)
