import logging
from pathlib import Path


class Logger:
    _PATH = Path(__file__).resolve().parent.parent / "app.log"

    @classmethod
    def configurar(cls):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[
                logging.FileHandler(cls._PATH, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

    @classmethod
    def leer_ultimos_logs(cls, n=50):
        with open(cls._PATH, encoding="utf-8") as f:
            lineas = f.readlines()

        return lineas[-n:]
