from pathlib import Path

from src.crm.utilidades import GestorArchivos

from . import ClienteCorporativo, ClientePremium, ClienteRegular


class RepositorioCliente:
    _PATH = Path(__file__).resolve().parent / "clientes.json"

    def __init__(self):
        datos = GestorArchivos.leer_json(self._PATH, default=[])
        self._clientes = [self._reconstruir_cliente(d) for d in datos]

    def _reconstruir_cliente(self, cliente):
        """Crea un objeto Cliente a partir de su forma diccionario."""
        cliente = cliente.copy()
        tipo = cliente.pop("tipo", "Regular")

        if tipo == "Premium":
            return ClientePremium(**cliente)
        if tipo == "Corporativo":
            return ClienteCorporativo(**cliente)
        return ClienteRegular(**cliente)

    def _guardar(self):
        """Convierte los Clientes a formato JSON y los persiste en fichero."""
        datos = [cliente.a_diccionario() for cliente in self._clientes]
        GestorArchivos.guardar_json(self._PATH, datos)

    def obtener_todos(self):
        """Retorna una lista con todos los clientes registrados."""
        return self._clientes

    def buscar_por_rut(self, rut: str):
        """Retorna el Cliente que posee el RUT indicado."""
        cliente = next((c for c in self._clientes if c.rut == rut), None)
        return cliente

    def eliminar_uno(self, rut: str):
        """Elimina el Cliente con el RUT indicado."""
        cantidad_original = len(self._clientes)

        self._clientes = [c for c in self._clientes if c.rut != rut]

        if len(self._clientes) == cantidad_original:
            return False

        self._guardar()
        return True

    def crear_uno(
        self, cliente: ClienteCorporativo | ClientePremium | ClienteRegular
    ):
        """Registra un nuevo Cliente en el sistema."""
        self._clientes.append(cliente)
        self._guardar()

    def reemplazar(
        self, cliente: ClienteCorporativo | ClientePremium | ClienteRegular
    ):
        """Busca un cliente y lo reemplaza por una nueva instancia con los datos editados."""
        for i, c in enumerate(self._clientes):
            if c.rut == cliente.rut:
                self._clientes[i] = cliente
                self._guardar()
                return
