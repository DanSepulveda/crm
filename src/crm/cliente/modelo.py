import re
from itertools import cycle

from src.crm.direccion import Direccion


class Cliente:
    TIPO = "Genérico"

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        telefono: str,
        direccion: Direccion,
    ):
        self._rut = self._validar_y_formatear_rut(rut)
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self) -> str:
        return f"Cliente {self.TIPO} - {self.nombre_completo}"

    def __eq__(self, cliente: object) -> bool:
        """Dos clientes son iguales si tienen el mismo RUT."""
        if not isinstance(cliente, Cliente):
            return NotImplemented
        return self.rut == cliente.rut

    @classmethod
    def _validar_y_formatear_rut(cls, rut: str) -> str:
        """Valida un RUT y lo retorna con un formato único."""
        rut = rut.replace(".", "").replace(" ", "").upper()

        if not cls._es_rut_valido(rut):
            raise ValueError("RUT inválido.")

        return rut

    @classmethod
    def desde_dict(cls, datos: dict) -> "Cliente":
        """Crea una instancia de Cliente a partir de un diccionario."""
        direccion = Direccion.desde_dict(datos["direccion"])

        return cls(
            rut=datos["rut"],
            nombres=datos["nombres"],
            apellido_paterno=datos["apellido_paterno"],
            apellido_materno=datos["apellido_materno"],
            correo=datos["correo"],
            telefono=datos["telefono"],
            direccion=direccion,
        )

    @staticmethod
    def _es_rut_valido(rut: str) -> bool:
        """Verifica la validez del RUT indicado."""
        if not rut:
            return False

        if not re.match(r"^\d{7,8}-[\dK]$", rut):
            return False

        parte_inicial, digito_verificador = rut.split("-")
        factores = cycle([2, 3, 4, 5, 6, 7])

        suma = sum(int(d) * next(factores) for d in reversed(parte_inicial))
        resultado = 11 - (suma % 11)

        if resultado == 11:
            return digito_verificador == "0"
        if resultado == 10:
            return digito_verificador == "K"

        return digito_verificador == str(resultado)

    @staticmethod
    def _validar_nombre(valor: str, nombre_campo: str) -> str:
        """Retorna texto formateado luego de validarlo (para nombres y apellidos.)"""
        if not valor or not valor.strip():
            raise ValueError(f"{nombre_campo} es obligatorio.")

        valor = " ".join(valor.strip().split())

        if len(valor) < 2:
            raise ValueError(f"{nombre_campo}: mínimo 2 caracteres")

        if len(valor) > 50:
            raise ValueError(f"{nombre_campo}: Demasiado largo.")

        if not valor.replace(" ", "").isalpha():
            raise ValueError(f"{nombre_campo}: solo letras y espacios.")

        return valor.title()

    @property
    def nombre_completo(self) -> str:
        return " ".join(
            (self.nombres, self.apellido_paterno, self.apellido_materno)
        )

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombres(self) -> str:
        return self._nombres

    @nombres.setter
    def nombres(self, nuevo_nombre: str):
        self._nombres = self._validar_nombre(
            nuevo_nombre, nombre_campo="Nombres"
        )

    @property
    def apellido_paterno(self) -> str:
        return self._apellido_paterno

    @apellido_paterno.setter
    def apellido_paterno(self, nuevo_apellido: str):
        self._apellido_paterno = self._validar_nombre(
            nuevo_apellido, nombre_campo="Apellido Paterno"
        )

    @property
    def apellido_materno(self) -> str:
        return self._apellido_materno

    @apellido_materno.setter
    def apellido_materno(self, nuevo_apellido):
        self._apellido_materno = self._validar_nombre(
            nuevo_apellido, nombre_campo="Apellido Materno"
        )

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo: str):
        nuevo_correo = nuevo_correo.strip().lower()

        if not re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w{2,}", nuevo_correo):
            raise ValueError("Correo inválido.")

        self._correo = nuevo_correo

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono: str):
        nuevo_telefono = nuevo_telefono.strip().replace(" ", "")

        if not re.fullmatch(r"(?:\+?56)?9\d{8}", nuevo_telefono):
            raise ValueError("Teléfono inválido.")

        if nuevo_telefono.startswith("9"):
            nuevo_telefono = "+56" + nuevo_telefono
        elif nuevo_telefono.startswith("56"):
            nuevo_telefono = "+" + nuevo_telefono

        self._telefono = nuevo_telefono

    @property
    def direccion(self) -> "Direccion":
        return self._direccion

    @direccion.setter
    def direccion(self, nueva_direccion: Direccion):
        if not isinstance(nueva_direccion, Direccion):
            raise ValueError("Se requiere un objeto de la clase Direccion.")

        self._direccion = nueva_direccion

    def a_dict(self):
        """Retorna el objeto Cliente en formato dict"""
        return {
            "tipo": self.TIPO,
            "rut": self.rut,
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "correo": self.correo,
            "telefono": self.telefono,
            "direccion": self.direccion.a_dict(),
        }


class ClienteRegular(Cliente):
    TIPO = "Regular"

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        telefono: str,
        direccion: Direccion,
    ):
        super().__init__(
            rut,
            nombres,
            apellido_paterno,
            apellido_materno,
            correo,
            telefono,
            direccion,
        )


class ClientePremium(Cliente):
    TIPO = "Premium"

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        telefono: str,
        direccion: Direccion,
        puntos: int = 0,
    ):
        super().__init__(
            rut,
            nombres,
            apellido_paterno,
            apellido_materno,
            correo,
            telefono,
            direccion,
        )
        self.puntos = puntos


class ClienteCorporativo(Cliente):
    TIPO = "Corporativo"

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellido_paterno: str,
        apellido_materno: str,
        correo: str,
        telefono: str,
        direccion: Direccion,
    ):
        super().__init__(
            rut,
            nombres,
            apellido_paterno,
            apellido_materno,
            correo,
            telefono,
            direccion,
        )
