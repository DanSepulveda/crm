from .repositorio import RepositorioCliente


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
