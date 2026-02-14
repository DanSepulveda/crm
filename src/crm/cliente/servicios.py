import logging
from dataclasses import dataclass

from . import (
    ClienteCorporativo,
    ClientePremium,
    ClienteRegular,
    RepositorioCliente,
)


logger = logging.getLogger(__name__)


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

    def _reconstruir_cliente(self, datos):
        """Crea un Cliente a partir de un diccionario plano."""
        datos = datos.copy()

        direccion = {
            "calle": datos.pop("calle"),
            "numero": datos.pop("numero"),
            "region": datos.pop("region"),
            "comuna": datos.pop("comuna"),
        }
        datos["direccion"] = direccion
        tipo = datos.pop("tipo", "Regular")

        clase = self._MAPA_TIPOS[tipo]
        return clase(**datos)

    def hay_cambios(self, datos) -> bool:
        """Verifica si se ha modificado el usuario (comprobar el formulario)."""
        try:
            cliente_original = self._repo.buscar_por_rut(datos["rut"])
            cliente_editado = self._reconstruir_cliente(datos)
            if not cliente_original:
                return False
            return (
                cliente_original.a_diccionario()
                != cliente_editado.a_diccionario()
            )
        except ValueError:
            return False

    def obtener_uno(self, rut: str):
        """Retorna el cliente con el RUT indicado."""
        return self._repo.buscar_por_rut(rut)

    def obtener_todos(self):
        """Retorna todos los clientes registrados."""
        datos = self._repo.obtener_todos() or []
        return datos

    def obtener_filtrados(self, busqueda: str = ""):
        """Retorna una lista de Clientes, buscando en sus nombres, apellidos o RUT."""
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
        """Elimina un Cliente, validando previamente que esté registrado."""
        eliminado = self._repo.eliminar_uno(rut)

        if not eliminado:
            logger.warning("Se ha intentado eliminar cliente no registrado.")
            return RespuestaServicio(False, "Cliente no encontrado.")

        logger.info(f"Cliente eliminado. RUT: {rut}")
        return RespuestaServicio(True, "Cliente eliminado correctamente.")

    def registrar_cliente(self, datos) -> RespuestaServicio:
        """Registra un nuevo Cliente, validando que no se encuentre registrado."""
        try:
            existe_usuario = self._repo.buscar_por_rut(datos["rut"])
            if existe_usuario:
                logger.warning(
                    f"Creación fallida. El cliente RUT: {datos['rut']} ya se encuentra registrado."
                )
                raise ValueError("El RUT ya se encuentra registrado.")

            cliente = self._reconstruir_cliente(datos)
            self._repo.crear_uno(cliente)
            logger.info(f"Nuevo cliente registrado. RUT: {datos['rut']}")
            return RespuestaServicio(True, "Cliente creado correctamente.")
        except ValueError as e:
            return RespuestaServicio(False, str(e))

    def editar_cliente(self, datos) -> RespuestaServicio:
        """Actualiza los datos de un Cliente, validando que esté registrado."""
        try:
            cliente_original = self._repo.buscar_por_rut(datos["rut"])
            if cliente_original is None:
                logger.warning(
                    "Se ha intentado modificar cliente no registrado."
                )
                raise ValueError("Cliente no registrado.")

            cliente_editado = self._reconstruir_cliente(datos)
            if (
                cliente_original.a_diccionario()
                == cliente_editado.a_diccionario()
            ):
                raise ValueError("No hay cambios para guardar.")

            self._repo.reemplazar(cliente_editado)
            logger.info(f"Cliente modificado. RUT: {datos['rut']}")
            return RespuestaServicio(True, "Cliente editado correctamente.")
        except ValueError as e:
            return RespuestaServicio(False, str(e))
