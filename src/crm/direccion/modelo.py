from pathlib import Path
from typing import TypedDict

from src.crm.utilidades import GestorArchivos


Regiones = dict[str, list[str]]


class DictDireccion(TypedDict):
    calle: str
    numero: str
    region: str
    comuna: str


class Direccion:
    _PATH = Path(__file__).parent / "regiones.json"
    _MAPA_TERRITORIAL: Regiones = GestorArchivos.leer_json(_PATH, default={})

    def __init__(self, calle: str, numero: str, region: str, comuna: str):
        self.calle = calle
        self.numero = numero
        self.actualizar_ubicacion(region, comuna)

    def __str__(self):
        return f"{self.calle} #{self.numero}, {self.comuna}, {self.region}."

    @classmethod
    def obtener_regiones(cls) -> list[str]:
        """Devuelve una lista con todas las regiones."""
        return list(cls._MAPA_TERRITORIAL.keys())

    @classmethod
    def obtener_comunas_por_region(cls, region: str) -> list[str]:
        """Devuelve la lista de comunas de una región específica."""
        return cls._MAPA_TERRITORIAL.get(region, [])

    @classmethod
    def desde_dict(cls, datos: DictDireccion) -> "Direccion":
        """Crea uns instancia de Direccion a partir de un diccionario."""
        return cls(**datos)

    @classmethod
    def _validar_region(cls, region: str):
        """Verifica la validez de una región (que exista)."""
        if region not in cls._MAPA_TERRITORIAL:
            raise ValueError("Región no existe.")

    @classmethod
    def _validar_comuna(cls, region: str, comuna: str):
        """Verifica que la comuna pertenezca a la región indicada"""
        comunas = cls.obtener_comunas_por_region(region)
        if comuna not in comunas:
            raise ValueError(f"{comuna} no pertenece a {region}.")

    @property
    def calle(self):
        return self._calle

    @calle.setter
    def calle(self, nueva_calle: str):
        valor_limpio = nueva_calle.strip()
        self._calle = valor_limpio if valor_limpio else "Sin calle"

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, nuevo_numero: str):
        valor_limpio = nuevo_numero.strip()
        self._numero = valor_limpio if valor_limpio else "Sin número"

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

    def a_dict(self) -> DictDireccion:
        """Retorna una dirección en formato diccionario."""
        return {
            "calle": self.calle,
            "numero": self.numero,
            "region": self.region,
            "comuna": self.comuna,
        }
