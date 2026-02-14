from .cliente import Cliente


class ClientePremium(Cliente):
    TIPO = "Premium"
    MAX_DESCUENTO = 50

    def __init__(self, *args, porcentaje_descuento: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.porcentaje_descuento = porcentaje_descuento

    @property
    def porcentaje_descuento(self) -> int:
        return self._porcentaje_descuento

    @porcentaje_descuento.setter
    def porcentaje_descuento(self, porcentaje: int | str):
        self._validar_cantidad_positiva(
            porcentaje, "Porcentaje descuento", permitir_cero=True
        )

        porcentaje = int(porcentaje)
        if porcentaje > self.MAX_DESCUENTO:
            raise ValueError(
                f"El descuento no puede superar el {self.MAX_DESCUENTO}%."
            )

        self._porcentaje_descuento = porcentaje

    def a_diccionario(self):
        """Retorna el objeto ClientePremium en formato diccionario."""
        diccionario = super().a_diccionario()
        diccionario.update({"porcentaje_descuento": self.porcentaje_descuento})
        return diccionario

    def calcular_descuento(self, monto: int | str) -> int:
        """Retorna el descuento aplicado a un monto."""
        self._validar_cantidad_positiva(monto, "Monto", permitir_cero=False)
        monto = int(monto)
        descuento = round(monto * self.porcentaje_descuento / 100)
        return descuento
