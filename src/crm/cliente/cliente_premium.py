from .cliente import Cliente


class ClientePremium(Cliente):
    TIPO = "Premium"
    MAX_DESCUENTO = 0.5

    def __init__(self, *args, porcentaje_descuento: float = 0.1, **kwargs):
        super().__init__(*args, **kwargs)
        self.porcentaje_descuento = porcentaje_descuento

    @property
    def porcentaje_descuento(self) -> float:
        return self._porcentaje_descuento

    @porcentaje_descuento.setter
    def porcentaje_descuento(self, porcentaje: float):
        if not isinstance(porcentaje, (int, float)):
            raise ValueError("Debe ingresar un valor numérico.")

        if porcentaje < 0:
            raise ValueError("El descuento no puede ser negativo.")

        if porcentaje > self.MAX_DESCUENTO:
            formato = f"{self.MAX_DESCUENTO * 100:.0f}"
            raise ValueError(f"El descuento no puede superar el {formato}%.")

        self._porcentaje_descuento = float(porcentaje)

    def aplicar_descuento(self, monto: int) -> int:
        """Retorna el monto luego de aplicado el descuento."""
        if not isinstance(monto, int):
            raise ValueError("El monto debe ser entero.")

        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")

        descuento = int(monto * self.porcentaje_descuento)
        return monto - descuento

    def a_dict(self):
        """Retorna el objeto ClientePremium en formato diccionario."""
        diccionario = super().a_dict()
        diccionario.update({"porcentaje_descuento": self.porcentaje_descuento})
        return diccionario
