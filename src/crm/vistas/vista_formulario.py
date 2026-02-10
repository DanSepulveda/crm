import platform
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from src.crm.cliente import Direccion
from src.crm.utilidades import ComponentesTkinter as Ctk


# Se importa App solo en desarrollo para poder usar su tipo. En tiempo de
# ejecución se ignora el import ya que genera dependencia circular
if TYPE_CHECKING:
    from src.crm.app import App


class VistaFormulario(ttk.Frame):
    def __init__(self, padre, app: "App"):
        super().__init__(padre)
        self._app = app
        self._campos = {}
        regiones = Direccion.obtener_regiones()

        # Configuración de filas y columnas para centrar el formulario
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)

        # Configuración de canvas (especie de frame que permite scroll)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.grid(column=1, row=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.grid(column=2, row=0, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        frame_form = ttk.Frame(self.canvas, padding=(0, 0, 0, 40))
        self.canvas.create_window((0, 0), window=frame_form, anchor="nw")

        # 1) SECCIÓN PARA TIPO DE CLIENTE Y SU ATRIBUTO DIFERENCIADOR
        self.fr_atributos = ttk.LabelFrame(
            frame_form, text="Cliente", padding=20
        )
        self.fr_atributos.pack()

        self._campos["tipo"] = Ctk.combo(
            self.fr_atributos,
            "Tipo de cliente",
            columna=0,
            fila=0,
            valores=["Regular", "Premium", "Corporativo"],
        )
        Ctk.campo(self.fr_atributos, "-", columna=1, fila=0, state="disabled")
        Ctk.separador_horizontal(frame_form)

        # 2) SECCIÓN PARA DATOS PERSONALES (nombres, apellidos, rut)
        fr_info = ttk.LabelFrame(
            frame_form, text="Información Personal", padding=20
        )
        fr_info.pack()

        self._campos["rut"] = Ctk.campo(
            fr_info, "RUT", columna=0, fila=0, mb=True
        )
        self._campos["nombre"] = Ctk.campo(
            fr_info, "Nombres", columna=1, fila=0, mb=True
        )
        self._campos["apellido_paterno"] = Ctk.campo(
            fr_info, "Apellido Paterno", columna=0, fila=1
        )
        self._campos["apellido_materno"] = Ctk.campo(
            fr_info, "Apellido Materno", 1, 1
        )
        Ctk.separador_horizontal(frame_form)

        # 3) SECCIÓN PARA DATOS DE CONTACTO (correo, teléfono)
        fr_contacto = ttk.LabelFrame(
            frame_form, text="Datos Contacto", padding=20
        )
        fr_contacto.pack()

        self._campos["correo"] = Ctk.campo(
            fr_contacto, "Correo electrónico", columna=0, fila=0
        )
        self._campos["telefono"] = Ctk.campo(
            fr_contacto, "Teléfono", columna=1, fila=0
        )
        Ctk.separador_horizontal(frame_form)

        # 4) SECCIÓN PARA DIRECCIÓN (calle, número, región, comuna)
        fr_dir = ttk.LabelFrame(frame_form, text="Dirección", padding=20)
        fr_dir.pack()

        self._campos["calle"] = Ctk.campo(
            fr_dir, "Calle", columna=0, fila=0, mb=True
        )
        self._campos["numero"] = Ctk.campo(
            fr_dir, "Número", columna=1, fila=0, mb=True
        )
        self._campos["region"] = Ctk.combo(
            fr_dir, "Región", columna=0, fila=1, valores=regiones
        )
        self._campos["comuna"] = Ctk.combo(
            fr_dir, "Comuna", columna=1, fila=1, valores=[]
        )
        Ctk.separador_horizontal(frame_form)

        # 5) LABEL PARA MENSAJE DE ERROR (por dato erróneo en formulario)
        self.label_estado = ttk.Label(frame_form, text="")
        self.label_estado.pack()

        # 6) SECCIÓN PARA BOTONES (crear/editar, cancelar)
        fr_botones = ttk.Frame(frame_form)
        fr_botones.pack(fill="x", expand=True)

        ttk.Button(
            fr_botones, text="Crear usuario", command=self._handle_guardar
        ).pack(side="right")

        ttk.Button(
            fr_botones, text="Cancelar", command=self._handle_cancelar
        ).pack(side="right", padx=10)

        # ------------------------------ EVENTOS ------------------------------
        # - actualizar opciones de comunas cuando se cambia la región
        self._campos["region"].bind(
            "<<ComboboxSelected>>", self._actualizar_comunas
        )

        # - cambiar entry (puntos, descuento, crédito) cuando se cambia el tipo de cliente
        self._campos["tipo"].bind(
            "<<ComboboxSelected>>", self._generar_campo_cliente
        )

        # - configuración del canvas para que el scroll funcione correctamente
        frame_form.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        # - configuración para que el scroll funcione con la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._handle_scroll)

        # ----------------------------- FIN INIT ------------------------------

    def _actualizar_comunas(self, _):
        region: str = self._campos["region"].get()
        comunas = Direccion.obtener_comunas_por_region(region)
        self._campos["comuna"]["values"] = comunas
        self._campos["comuna"].set("")

    def _leer_formulario(self) -> dict:
        return {clave: widget.get() for clave, widget in self._campos.items()}

    def _handle_guardar(self):
        formulario = self._leer_formulario()
        print(formulario)

        # try:
        #     if any(e == "" for e in entradas.values()):
        #         raise ValueError("Todos los campos son obligatorios.")
        #     respuesta = self.app.servicio_cliente.registrar_cliente(**entradas)
        #     print(respuesta)
        # except ValueError as e:
        #     self.label_estado.config(text=str(e))

    def _handle_cancelar(self):
        pass

    def _handle_scroll(self, evento):
        os = platform.system()
        factor = evento.delta / 120 if os == "Windows" else evento.delta
        self.canvas.yview_scroll(int(-1 * factor), "units")

    def _generar_campo_cliente(self, _):
        tipo = self._campos["tipo"].get()
        tipos = {
            "Regular": ("puntos", "Puntos disponibles"),
            "Premium": ("porcentaje_descuento", "Porcentaje de descuento"),
            "Corporativo": ("limite_credito", "Límite de crédito"),
        }

        # quitar propiedades extras de self._campos (dejar solo con campos comunes)
        for clave in [c[0] for c in tipos.values()]:
            self._campos.pop(clave, None)

        # agregar propiedad a self._campos dependiendo del tipo de cliente
        tipo = tipos.get(tipo, tipos["Regular"])
        self._campos[tipo[0]] = Ctk.campo(
            self.fr_atributos, tipo[1], columna=1, fila=0
        )
        print(self._campos.keys())
