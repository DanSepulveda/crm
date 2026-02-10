from pathlib import Path
from typing import TypedDict

from src.crm.utilidades import GestorArchivos


class DictDireccion(TypedDict):
    calle: str
    numero: str
    region: str
    comuna: str


class Direccion:
    _PATH = Path(__file__).parent / "regiones.json"
    _MAPA_TERRITORIAL: dict[str, list[str]] = GestorArchivos.leer_json(
        _PATH, default={}
    )

    def __init__(self, calle: str, numero: str, region: str, comuna: str):
        self.calle = calle
        self.numero = numero
        self.actualizar_ubicacion(region, comuna)

    def __str__(self):
        return f"{self.calle} #{self.numero}, {self.comuna}, {self.region}."

    @classmethod
    def obtener_regiones(cls) -> list[str]:
        """Retorna una lista con todas las regiones."""
        return list(cls._MAPA_TERRITORIAL.keys())

    @classmethod
    def obtener_comunas_por_region(cls, region: str) -> list[str]:
        """Rotorna la lista de comunas de la región indicada."""
        return cls._MAPA_TERRITORIAL.get(region, [])

    @classmethod
    def _validar_region(cls, region: str):
        """Verifica la validez de una región (que exista)."""
        if not region:
            raise ValueError("Debe indicar la región.")
        if region not in cls._MAPA_TERRITORIAL:
            raise ValueError("Región no existe.")

    @classmethod
    def _validar_comuna(cls, region: str, comuna: str):
        """Verifica que la comuna pertenezca a la región indicada."""
        if not region:
            raise ValueError("Debe indicar la región.")
        if not comuna:
            raise ValueError("Debe indicar la comuna.")

        comunas = cls.obtener_comunas_por_region(region)

        if comuna not in comunas:
            raise ValueError(f"{comuna} no pertenece a {region}.")

    @property
    def calle(self):
        return self._calle

    @calle.setter
    def calle(self, nueva_calle: str):
        valor_limpio = nueva_calle.strip()
        if not valor_limpio:
            raise ValueError("Debe indicar nombre de calle.")
        self._calle = valor_limpio

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, nuevo_numero: str):
        valor_limpio = nuevo_numero.strip()
        self._numero = valor_limpio if valor_limpio else ""

    @property
    def region(self):
        return self._region

    @property
    def comuna(self):
        return self._comuna

    def actualizar_ubicacion(self, nueva_region: str, nueva_comuna: str):
        """Cambia región y comuna, asegurando que la combinación sea válida."""
        self._validar_region(nueva_region)
        self._validar_comuna(nueva_region, nueva_comuna)
        self._region = nueva_region
        self._comuna = nueva_comuna

    def a_diccionario(self) -> DictDireccion:
        """Retorna una Direccion en formato diccionario."""
        return {
            "calle": self.calle,
            "numero": self.numero,
            "region": self.region,
            "comuna": self.comuna,
        }
