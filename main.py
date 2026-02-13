from src.crm.app import App
from src.crm.cliente import RepositorioCliente, ServicioCliente
from src.crm.utilidades import Logger


def main():
    Logger.configurar()
    repo = RepositorioCliente()
    servicio = ServicioCliente(repo)
    app = App(servicio_cliente=servicio)
    app.mainloop()


if __name__ == "__main__":
    main()
