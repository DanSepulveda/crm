from pathlib import Path

from src.crm.utilidades import GestorArchivos

from .cliente_corporativo import ClienteCorporativo
from .cliente_premium import ClientePremium
from .cliente_regular import ClienteRegular


class RepositorioCliente:
    _PATH = Path(__file__).resolve().parent / "clientes.json"

    def __init__(self):
        self._clientes = GestorArchivos.leer_json(self._PATH, default=[])

    def _crear_cliente(self, cliente):
        cliente = cliente.copy()
        tipo = cliente.pop("tipo", "Genérico")

        if tipo == "Premium":
            return ClientePremium.desde_dict(cliente)
        if tipo == "Corporativo":
            return ClienteCorporativo.desde_dict(cliente)
        return ClienteRegular.desde_dict(cliente)

    def obtener_todos(self):
        return [self._crear_cliente(data) for data in self._clientes]

    def buscar_por_rut(self, rut: str):
        cliente = next((c for c in self._clientes if c["rut"] == rut), None)
        return self._crear_cliente(cliente) if cliente else None

    def eliminar_uno(self, rut: str):
        cantidad_original = len(self._clientes)

        self._clientes = [c for c in self._clientes if c["rut"] != rut]

        if len(self._clientes) == cantidad_original:
            return False

        GestorArchivos.guardar_json(self._PATH, self._clientes)
        return True
