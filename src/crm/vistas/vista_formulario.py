import platform
import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from src.crm.cliente import Direccion
from src.crm.utilidades import ComponentesTkinter as Ctk


# Se importa App solo en desarrollo para poder usar su tipo. En tiempo de
# ejecución se ignora el import ya que genera dependencia circular
if TYPE_CHECKING:
    from src.crm.app import App


def esta_vacio(dic: dict) -> bool:
    return all(
        esta_vacio(v) if isinstance(v, dict) else not v for v in dic.values()
    )


class VistaFormulario(ttk.Frame):
    def __init__(self, padre, app: "App"):
        super().__init__(padre)
        self._app = app
        self._campos = {}
        self._modo_edicion = False
        self._cliente_actual = None
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
        self._campos["nombres"] = Ctk.campo(
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
            fr_botones, text="Crear usuario", command=self._onclick_guardar
        ).pack(side="right")

        ttk.Button(
            fr_botones, text="Cancelar", command=self._onclick_cancelar
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
        self.canvas.bind_all("<MouseWheel>", self._onscroll)

    def preparar_creacion(self):
        self._modo_edicion = False
        self._cliente_actual = None
        self._limpiar_formulario()

    def _actualizar_comunas(self, _):
        """Cambia las opciones de comunas al momento de cambiar la región."""
        region: str = self._campos["region"].get()
        comunas = Direccion.obtener_comunas_por_region(region)
        self._campos["comuna"]["values"] = comunas
        self._campos["comuna"].set("")

    def _leer_formulario(self) -> dict:
        """Retorna un diccionario con los datos del formulario."""
        return {clave: widget.get() for clave, widget in self._campos.items()}

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        for campo in self._campos.values():
            if isinstance(campo, ttk.Combobox):
                campo.set("")
            else:
                campo.delete(0, tk.END)

    def _onscroll(self, evento):
        """Controla la velocidad del scroll al usar la rueda del mouse."""
        os = platform.system()
        factor = evento.delta / 120 if os == "Windows" else evento.delta
        self.canvas.yview_scroll(int(-1 * factor), "units")

    def _onclick_guardar(self):
        """Ejecuta el servicio de creación/edición de cliente."""
        datos = self._leer_formulario()

        if self._modo_edicion:
            # TODO
            # respuesta = self._app._servicio_cliente.editar_cliente(datos)
            pass
        else:
            respuesta = self._app._servicio_cliente.registrar_cliente(datos)

        if respuesta.exito:
            messagebox.showinfo("OK", respuesta.mensaje)
            self._limpiar_formulario()
            self._app._mostrar_vista("VistaClientes")
        else:
            messagebox.showerror("ERROR", respuesta.mensaje)

    def _onclick_cancelar(self):
        """Redirige al menú principal, validando que no hayan datos sin guardar."""
        if self._modo_edicion:
            # TODO
            pass
        else:
            form_vacio = esta_vacio(self._leer_formulario())
            if not form_vacio:
                confirmar = messagebox.askokcancel(
                    "Advertencia",
                    "Tiene datos sin guardar. Si continúa, se eliminarán.",
                )
                if not confirmar:
                    return
        self._app._mostrar_vista("VistaClientes")

    def _generar_campo_cliente(self, _):
        """Agrega un campo para un atributo, dependiendo del tipo de cliente."""
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
