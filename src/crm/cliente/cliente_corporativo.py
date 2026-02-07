from .cliente import Cliente


class ClienteCorporativo(Cliente):
    TIPO = "Corporativo"
    MAX_LIMITE = 10_000_000

    def __init__(
        self, *args, razon_social: str, limite_credito: int = 0, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.razon_social = razon_social
        self.limite_credito = limite_credito

    @property
    def razon_social(self) -> str:
        return self._razon_social

    @razon_social.setter
    def razon_social(self, nueva_razon: str):
        if not isinstance(nueva_razon, str):
            raise ValueError("Razón social inválida.")

        valor_limpio = " ".join(nueva_razon.strip().split())

        if not valor_limpio:
            raise ValueError("La razón social es obligatoria.")

        if len(valor_limpio) < 5:
            raise ValueError("Razón social demasiado corta.")

        if len(valor_limpio) > 100:
            raise ValueError("Razón social demasiado larga.")

        self._razon_social = valor_limpio

    @property
    def limite_credito(self) -> int:
        return self._limite_credito

    @limite_credito.setter
    def limite_credito(self, nuevo_limite: int):
        if not isinstance(nuevo_limite, int):
            raise ValueError("Límite de crédito inválido.")

        if nuevo_limite < 0:
            raise ValueError("El límite de crédito no puede ser negativo.")

        if nuevo_limite > self.MAX_LIMITE:
            formateado = f"{self.MAX_LIMITE:,}".replace(",", ".")
            raise ValueError(f"Límite excede el máximo (${formateado}).")

        self._limite_credito = nuevo_limite

    def a_dict(self):
        """Retorna el objeto ClienteCorporativo en formato diccionario."""
        diccionario = super().a_dict()
        diccionario.update(
            {
                "razon_social": self.razon_social,
                "limite_credito": self.limite_credito,
            }
        )
        return diccionario
