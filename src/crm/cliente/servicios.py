from dataclasses import dataclass

from .repositorio import RepositorioCliente


@dataclass
class RespuestaServicio:
    exito: bool
    mensaje: str


class ServicioCliente:
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
            return RespuestaServicio(
                exito=False, mensaje="Cliente no encontrado."
            )

        return RespuestaServicio(
            exito=True, mensaje="Cliente eliminado correctamente."
        )
