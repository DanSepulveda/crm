from .cliente import Cliente


class ClienteRegular(Cliente):
    TIPO = "Regular"

    def __init__(self, *args, puntos: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self.puntos = puntos

    def __str__(self) -> str:
        return f"{super().__str__()} - Puntos: {self.puntos}"

    @staticmethod
    def _validar_cantidad_positiva(valor: int, permitir_cero: bool = False):
        if not isinstance(valor, int):
            raise ValueError("Debe ingresar un número entero.")

        if permitir_cero:
            if valor < 0:
                raise ValueError("Debe ingresar un número positivo.")
        else:
            if valor <= 0:
                raise ValueError("Debe ingresar un número mayor que cero.")

    @property
    def puntos(self) -> int:
        return self._puntos

    @puntos.setter
    def puntos(self, cantidad: int):
        self._validar_cantidad_positiva(cantidad, permitir_cero=True)
        self._puntos = cantidad

    def acumular_puntos(self, cantidad: int):
        self._validar_cantidad_positiva(cantidad)
        self._puntos += cantidad

    def utilizar_puntos(self, cantidad: int):
        self._validar_cantidad_positiva(cantidad)

        if cantidad > self.puntos:
            raise ValueError("Puntos insuficientes.")

        self._puntos -= cantidad

    def a_dict(self):
        """Retorna el objeto ClienteRegular en formato diccionario."""
        diccionario = super().a_dict()
        diccionario.update({"puntos": self.puntos})
        return diccionario
