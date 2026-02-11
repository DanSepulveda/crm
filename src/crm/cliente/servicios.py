from dataclasses import dataclass

from . import ClienteCorporativo, ClientePremium, ClienteRegular
from .repositorio import RepositorioCliente


@dataclass
class RespuestaServicio:
    exito: bool
    mensaje: str


class ServicioCliente:
    _MAPA_TIPOS = {
        "Regular": ClienteRegular,
        "Premium": ClientePremium,
        "Corporativo": ClienteCorporativo,
    }

    def __init__(self, repositorio: RepositorioCliente):
        self._repo = repositorio

    def obtener_todos(self):
        datos = self._repo.obtener_todos() or []
        return datos

    def obtener_filtrados(self, busqueda: str = ""):
        busqueda = busqueda.strip().lower()
        clientes = self.obtener_todos()

        return [
            c
            for c in clientes
            if busqueda in c.nombres.lower()
            or busqueda in c.apellido_paterno.lower()
            or busqueda in c.apellido_materno.lower()
            or busqueda in c.nombre_completo.lower()
            or busqueda in c.rut.lower()
        ]

    def eliminar_cliente(self, rut: str) -> RespuestaServicio:
        eliminado = self._repo.eliminar_uno(rut)

        if not eliminado:
            return RespuestaServicio(False, "Cliente no encontrado.")

        return RespuestaServicio(True, "Cliente eliminado correctamente.")

    def registrar_cliente(self, datos) -> RespuestaServicio:
        try:
            datos = datos.copy()

            existe_usuario = self._repo.buscar_por_rut(datos["rut"])
            if existe_usuario:
                raise ValueError("El RUT ya se encuentra registrado.")

            direccion = {
                "calle": datos.pop("calle"),
                "numero": datos.pop("numero"),
                "region": datos.pop("region"),
                "comuna": datos.pop("comuna"),
            }
            datos["direccion"] = direccion
            tipo = datos.pop("tipo", "Regular")

            clase = self._MAPA_TIPOS.get(tipo)
            if not clase:
                return RespuestaServicio(False, "Tipo de cliente inválido.")

            cliente = clase(**datos)
            self._repo.crear_uno(cliente)
            return RespuestaServicio(True, "Cliente creado correctamente.")
        except ValueError as e:
            return RespuestaServicio(False, str(e))
