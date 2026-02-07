from tkinter import ttk


class VistaClientes(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # -------------------------- FRAME CLIENTES ---------------------------
        frame_clientes = ttk.Frame(self)
        frame_clientes.grid(column=0, row=0, sticky="nsew")

        # 1) BUSCADOR
        self.buscador = ttk.Entry(frame_clientes, width=50)
        self.buscador.pack(pady=10)
        self.buscador.bind("<KeyRelease>", self._handle_busqueda)

        # 2) TABLA CLIENTES CON SCROLL
        # - frame para tabla y scroll
        self.frame_tabla = ttk.Frame(frame_clientes)
        self.frame_tabla.pack(padx=10, pady=10)

        # - scrollbar
        scroll_y = ttk.Scrollbar(self.frame_tabla)
        scroll_y.pack(side="right", fill="y")

        # - tabla
        columnas = [
            ("N°", 40, "e"),
            ("Tipo", 80, "center"),
            ("RUT", 150, "e"),
            ("Nombres", 150, "w"),
            ("Apellido paterno", 150, "w"),
            ("Apellido materno", 150, "w"),
        ]
        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=[c[0] for c in columnas],
            show="headings",
            yscrollcommand=scroll_y.set,
        )
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll_y.config(command=self.tabla.yview)

        # - agregar encabezados y configurar columnas
        for columna in columnas:
            nombre, ancho, posicion = columna
            self.tabla.column(nombre, width=ancho, anchor=posicion)  # type: ignore
            self.tabla.heading(nombre, text=nombre)

        # 3) LABEL PARA MENSAJE DE RESULTADO BÚSQUEDA
        self.resultado = ttk.Label(frame_clientes)

        # tabla.bind("<<TreeviewSelect>>", handle_click_fila)
        self._refrescar_tabla()

        # --------------------------- FRAME BOTONES ---------------------------
        frame_opciones = ttk.Frame(self)
        frame_opciones.grid(column=1, row=0, sticky="news", padx=10, pady=10)

        ttk.Button(frame_opciones, text="Crear Usuario", width=15).pack(
            pady=(0, 10)
        )

        ttk.Button(frame_opciones, text="Editar usuario", width=15).pack(
            pady=(0, 10)
        )

        ttk.Button(frame_opciones, text="Eliminar usuario", width=15).pack(
            pady=(0, 10)
        )

        ttk.Button(
            frame_opciones,
            text="Volver al inicio",
            width=15,
            command=lambda: self.app._mostrar_vista("VistaInicio"),
        ).pack(pady=(40, 0))

    def _refrescar_tabla(self, busqueda: str = ""):
        # 1) Vaciar la tabla
        self.tabla.delete(*self.tabla.get_children())

        # 2) Obtener clientes filtrados
        clientes = self.app.servicio_cliente.obtener_filtrados(busqueda)

        # 3) Mostrar resultado (clientes o mensaje)
        if not self.app.servicio_cliente.obtener_todos():
            self._mostrar_mensaje("No hay clientes registrados.")
        elif not clientes:
            self._mostrar_mensaje("Sin resultados para la búsqueda.")
        else:
            self.frame_tabla.pack()
            self.resultado.pack_forget()

            for i, c in enumerate(clientes, 1):
                self.tabla.insert(
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

    def _handle_busqueda(self, _):
        busqueda = self.buscador.get()
        self._refrescar_tabla(busqueda)

    def _mostrar_mensaje(self, mensaje: str):
        self.frame_tabla.pack_forget()
        self.resultado.config(text=mensaje)
        self.resultado.pack()
