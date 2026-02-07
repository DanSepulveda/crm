from pathlib import Path

from src.crm.utilidades import GestorArchivos

from .cliente_corporativo import ClienteCorporativo
from .cliente_premium import ClientePremium
from .cliente_regular import ClienteRegular


class RepositorioCliente:
    _PATH = Path(__file__).parent / "clientes.json"

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
