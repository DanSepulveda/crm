from dataclasses import dataclass

from . import (
    ClienteCorporativo,
    ClientePremium,
    ClienteRegular,
    RepositorioCliente,
)


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
        cliente_original = self._repo.buscar_por_rut(datos["rut"])
        cliente_editado = self._reconstruir_cliente(datos)
        if not cliente_original:
            return False
        return (
            cliente_original.a_diccionario() != cliente_editado.a_diccionario()
        )

    def obtener_uno(self, rut: str):
        return self._repo.buscar_por_rut(rut)

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
            existe_usuario = self._repo.buscar_por_rut(datos["rut"])
            if existe_usuario:
                raise ValueError("El RUT ya se encuentra registrado.")

            cliente = self._reconstruir_cliente(datos)
            self._repo.crear_uno(cliente)
            return RespuestaServicio(True, "Cliente creado correctamente.")
        except ValueError as e:
            return RespuestaServicio(False, str(e))

    def editar_cliente(self, datos) -> RespuestaServicio:
        cliente_original = self._repo.buscar_por_rut(datos["rut"])
        if cliente_original is None:
            return RespuestaServicio(False, "Cliente no registrado.")

        cliente_editado = self._reconstruir_cliente(datos)
        if cliente_original.a_diccionario() == cliente_editado.a_diccionario():
            return RespuestaServicio(False, "No hay cambios para guardar.")

        self._repo.reemplazar(cliente_editado)
        return RespuestaServicio(True, "Cliente editado correctamente.")
