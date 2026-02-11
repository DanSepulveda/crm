from .cliente import Cliente


class ClienteRegular(Cliente):
    TIPO = "Regular"

    def __init__(self, *args, puntos: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.puntos = puntos

    def __str__(self) -> str:
        return f"{super().__str__()} - Puntos: {self.puntos}"

    @staticmethod
    def _validar_cantidad_positiva(
        valor: int | str, nombre: str, permitir_cero: bool = False
    ):
        if (
            isinstance(valor, str)
            and not valor.isdigit()
            and not isinstance(valor, int)
        ):
            raise ValueError(f"'{nombre}' debe ser un número entero.")

        valor_numerico = int(valor)

        if permitir_cero:
            if valor_numerico < 0:
                raise ValueError(f"'{nombre}' debe ser mayor o igual que cero")
        else:
            if valor_numerico <= 0:
                raise ValueError(f"'{nombre}' debe ser mayor que cero.")

    @property
    def puntos(self) -> int:
        return self._puntos

    @puntos.setter
    def puntos(self, cantidad: int | str):
        self._validar_cantidad_positiva(cantidad, "Puntos", permitir_cero=True)
        self._puntos = int(cantidad)

    def a_diccionario(self) -> dict:
        """Retorna el objeto ClienteRegular en formato diccionario."""
        diccionario = super().a_diccionario()
        diccionario.update({"puntos": self.puntos})
        return diccionario

    def acumular_por_compra(self, monto: int | str) -> str:
        """Agrega puntos al Cliente dependiendo del monto de la compra."""
        self._validar_cantidad_positiva(monto, "Monto", permitir_cero=False)
        acumulados = int(monto) // 1000  # 1 punto cada $1.000
        self._puntos += acumulados
        return f"Ha acumulado {acumulados} puntos."
