import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Literal

from src.crm.utilidades import ComponentesTkinter as Ctk


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

        ttk.Label(frame_busqueda, text="Búsqueda", style="Entry.TLabel").pack(side="left")

        self._buscador = ttk.Entry(frame_busqueda)
        self._buscador.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # 2 -> label para mostrar resultado de búsqueda
        self._titulo = ttk.Label(frame_clientes, style="Titulo.TLabel")
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
            ("Tipo", 85, "center"),
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
                stretch=nombre == "Nombres",
            )
            self._tabla.heading(nombre, text=nombre + " " * 4 if nombre == "RUT" else nombre, anchor=posicion)

        self._buscador.bind("<KeyRelease>", self._onchange_busqueda)
        self._tabla.bind("<<TreeviewSelect>>", self._onclick_fila)

        # -------------------- FRAME BOTONES (DERECHA) ------------------------
        frame_opciones = ttk.Frame(self)
        frame_opciones.grid(column=1, row=0, sticky="n")

        ttk.Button(
            frame_opciones,
            text="Crear Usuario",
            width=22,
            style="Primary.TButton",
            command=self._app.mostrar_formulario_creacion,
        ).pack(pady=(0, 10))

        self._btn_editar = ttk.Button(
            frame_opciones,
            text="Editar usuario",
            width=22,
            state="disabled",
            style="Secondary.TButton",
            command=self._app.mostrar_formulario_edicion,
        )
        self._btn_editar.pack(pady=(0, 10))

        self._btn_eliminar = ttk.Button(
            frame_opciones,
            text="Eliminar usuario",
            width=22,
            state="disabled",
            style="Danger.TButton",
            command=self._onclick_eliminar,
        )
        self._btn_eliminar.pack(pady=(0, 10))

        ttk.Button(
            frame_opciones,
            text="Volver al inicio",
            width=22,
            style="Secondary.TButton",
            command=lambda: self._app.mostrar_vista("VistaInicio"),
        ).pack(pady=(0, 10))
        Ctk.separador_horizontal(frame_opciones)

        # Frame para venta
        self._frame_venta = ttk.Frame(frame_opciones)
        ttk.Label(
            self._frame_venta,
            text="Realizar venta",
            font=("Segoe UI", 12, "bold", "underline"),
        ).pack()
        self._beneficio = ttk.Label(self._frame_venta, style="Entry.TLabel")
        self._beneficio.pack(pady=10)
        frame_campo = ttk.Frame(self._frame_venta)
        frame_campo.pack()
        self._monto = Ctk.campo(frame_campo, "Monto de venta", 0, 0, width=18, mb=True)
        ttk.Button(
            self._frame_venta,
            text="Realizar venta",
            width=15,
            style="Primary.TButton",
            command=self._realizar_venta,
        ).pack()

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
                        c.rut + " " * 4,
                        c.nombres,
                        c.apellido_paterno,
                        c.apellido_materno,
                    ),
                    tags=('fila_par' if i % 2 == 0 else 'fila_impar')
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
            cliente = self._app.servicio_cliente.obtener_uno(rut_elegido)
            self._app.cliente_seleccionado = cliente
            estado = "normal"
            # Configuración para cuadro de VENTA
            beneficio = self._app.servicio_cliente.obtener_beneficio(cliente)
            self._beneficio.config(text=beneficio)
            self._monto.delete(0, tk.END)
            self._frame_venta.pack()
        else:
            self._app.cliente_seleccionado = None
            estado = "disabled"
            self._frame_venta.pack_forget()

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

    def _realizar_venta(self):
        monto = self._monto.get()
        cliente = self._app.cliente_seleccionado
        resultado = self._app.servicio_cliente.realizar_venta(monto, cliente)

        if resultado.exito:
            messagebox.showerror("Error", resultado.mensaje)
        else:
            messagebox.showinfo("Ok", resultado.mensaje)

        busqueda = self._buscador.get()
        self._refrescar_tabla(busqueda)
