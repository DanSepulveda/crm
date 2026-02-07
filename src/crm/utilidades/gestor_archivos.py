import json
from pathlib import Path
from typing import Any, TypeVar


T = TypeVar("T")


class GestorArchivos:
    @staticmethod
    def crear_directorio(ruta: str | Path) -> None:
        """Crea las carpetas (en caso de no existir) de la ruta indicada."""
        path = Path(ruta)
        path = path.parent if path.suffix else path
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def leer_json(ruta: str | Path, default: T) -> T:
        """Lee y retorna el contenido de un archivo .json"""
        try:
            with open(ruta, encoding="utf-8") as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    @classmethod
    def guardar_json(cls, ruta: str | Path, datos: Any):
        """Crea o sobrescribe un archivo .json en la ruta indicada."""
        try:
            cls.crear_directorio(ruta)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except OSError as e:
            raise OSError("Error al guardar JSON.") from e
