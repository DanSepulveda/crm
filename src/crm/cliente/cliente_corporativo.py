from .cliente import Cliente


class ClienteCorporativo(Cliente):
    TIPO = "Corporativo"
    MAX_LIMITE = 10_000_000

    def __init__(self, *args, limite_credito: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.limite_credito = limite_credito

    @property
    def limite_credito(self) -> int:
        return self._limite_credito

    @limite_credito.setter
    def limite_credito(self, limite: int | str):
        self._validar_cantidad_positiva(limite, "Límite de credito", True)
        limite = int(limite)

        if limite > self.MAX_LIMITE:
            formateado = f"{self.MAX_LIMITE:,}".replace(",", ".")
            raise ValueError(f"Crédito excede el máximo (${formateado}).")

        self._limite_credito = limite

    def a_diccionario(self):
        """Retorna el objeto ClienteCorporativo en formato diccionario."""
        diccionario = super().a_diccionario()
        diccionario.update({"limite_credito": self.limite_credito})
        return diccionario

    def utilizar_crédito(self, monto: int | str):
        """Descuenta crédito al realizar compras."""
        self._validar_cantidad_positiva(monto, "Monto")

        monto = int(monto)
        if monto > self.limite_credito:
            raise ValueError("El monto es mayor al crédito disponible.")

        self._limite_credito -= monto
