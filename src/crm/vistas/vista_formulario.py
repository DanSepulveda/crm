from tkinter import ttk

from src.crm.cliente import Direccion

from .ui import UI


class VistaFormulario(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre)
        self.app = app
        regiones = Direccion.obtener_regiones()

        # INFORMACIÓN PERSONAL
        fr_info = ttk.LabelFrame(self, text="Información Personal", padding=20)
        fr_info.grid(column=0, row=0)
        self.entry_rut = UI.campo(fr_info, "RUT", 0, 0, True)
        self.entry_nombres = UI.campo(fr_info, "Nombres", 1, 0, True)
        self.entry_paterno = UI.campo(fr_info, "Apellido Paterno", 0, 1)
        self.entry_materno = UI.campo(fr_info, "Apellido Materno", 1, 1)
        UI._separador(self, row=1)

        # DATOS DE CONTACTO
        fr_contacto = ttk.LabelFrame(self, text="Datos Contacto", padding=20)
        fr_contacto.grid(column=0, row=2)
        self.entry_correo = UI.campo(fr_contacto, "Correo", 0, 0)
        self.entry_telefono = UI.campo(fr_contacto, "Teléfono", 1, 0)
        UI._separador(self, row=3)

        # DIRECCION
        fr_dir = ttk.LabelFrame(self, text="Dirección", padding=20)
        fr_dir.grid(column=0, row=4)
        self.entry_calle = UI.campo(fr_dir, "Calle", 0, 0, True)
        self.entry_numero = UI.campo(fr_dir, "Número", 1, 0, True)
        self.entry_region = UI.combo(fr_dir, "Región", 0, 1, regiones)
        self.entry_comuna = UI.combo(fr_dir, "Comuna", 1, 1, [])
        UI._separador(self, row=5)

        self.entry_region.bind("<<ComboboxSelected>>", self.actualizar_comunas)

        self.label_estado = ttk.Label(self, text="")
        self.label_estado.grid(column=0, row=6)

        boton = ttk.Button(
            self, text="Crear usuario", command=self.handle_crear_usuario
        )
        boton.grid(column=0, row=7)

    def actualizar_comunas(self, _):
        region = self.entry_region.get()
        comunas = Direccion.obtener_comunas_por_region(region)
        self.entry_comuna["values"] = comunas
        self.entry_comuna.set("")

    def handle_crear_usuario(self):
        entradas = {
            "rut": self.entry_rut.get(),
            "nombres": self.entry_nombres.get(),
            "apellido_paterno": self.entry_paterno.get(),
            "apellido_materno": self.entry_materno.get(),
            "correo": self.entry_correo.get(),
            "telefono": self.entry_telefono.get(),
            "calle": self.entry_calle.get(),
            "numero": self.entry_numero.get(),
            "region": self.entry_region.get(),
            "comuna": self.entry_comuna.get(),
        }

        widgets = self.winfo_children()

        for i in widgets:
            print(isinstance(i, ttk.Entry))

        # try:
        #     if any(e == "" for e in entradas.values()):
        #         raise ValueError("Todos los campos son obligatorios.")
        #     respuesta = self.app.servicio_cliente.registrar_cliente(**entradas)
        #     print(respuesta)
        # except ValueError as e:
        #     self.label_estado.config(text=str(e))
