import json
from typing import TypedDict


Regiones = dict[str, list[str]]


class DictDireccion(TypedDict):
    calle: str
    numero: str
    region: str
    comuna: str | None


class Direccion:
    # 1) ATRIBUTOS DE CLASE
    try:
        with open("src/crm/direccion/regiones.json", encoding="utf-8") as f:
            MAPA_TERRITORIAL: Regiones = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        MAPA_TERRITORIAL: Regiones = {}
        raise RuntimeError("Error al cargar regiones.") from e

    # 2) MÉTODOS DUNDER
    def __init__(self, calle: str, numero: str, region: str, comuna: str):
        self.calle = calle
        self.numero = numero
        self.region = region
        self.comuna = comuna

    def __str__(self):
        return f"{self.calle} #{self.numero}, {self.comuna}, {self.region}."

    # 3) MÉTODOS DE CLASE
    @classmethod
    def obtener_regiones(cls):
        """Devuelve una lista con todas las regiones."""
        return list(cls.MAPA_TERRITORIAL.keys())

    @classmethod
    def obtener_comunas_por_region(cls, region: str):
        """Devuelve una lista de comunas para una región específica."""
        return cls.MAPA_TERRITORIAL.get(region, [])

    @classmethod
    def _validar_region(cls, region: str):
        """Verifica la validez de una región (que exista)."""
        if region not in cls.MAPA_TERRITORIAL:
            raise ValueError("Región no existe.")

    @classmethod
    def _validar_comuna(cls, region: str, comuna: str):
        """Verifica la validez de una comuna (que pertenezca a la región indicada)."""
        comunas = cls.obtener_comunas_por_region(region)
        if comuna not in comunas:
            raise ValueError(f"{comuna} no pertenece a {region}.")

    # 4) GETTERS Y SETTERS
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

    @region.setter
    def region(self, nueva_region: str):
        self._validar_region(nueva_region)

        # Si se cambia solo la región, sin utilizar el método
        # actualizar_ubicacion, se establece la comuna como None
        if hasattr(self, "_region") and self._region != nueva_region:
            self._comuna = None
            print("Región cambiada. Por favor, actualice la comuna.")

        self._region = nueva_region

    @property
    def comuna(self):
        return self._comuna

    @comuna.setter
    def comuna(self, nueva_comuna: str):
        if self._region is None:
            raise ValueError("Debe asignar una región previamente.")
        self._validar_comuna(self._region, nueva_comuna)
        self._comuna = nueva_comuna

    # 5) MÉTODOS DE INSTANCIA
    def actualizar_ubicacion(self, nueva_region, nueva_comuna):
        """Cambia región y comuna asegurando que la combinación sea válida."""
        self._validar_region(nueva_region)
        self._validar_comuna(nueva_region, nueva_comuna)
        self._region = nueva_region
        self._comuna = nueva_comuna

    def to_dict(self) -> DictDireccion:
        """Retorna una dirección en formato dict."""
        return {
            "calle": self.calle,
            "numero": self.numero,
            "region": self.region,
            "comuna": self.comuna,
        }
