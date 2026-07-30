

from smoke.ConstructorsErrorEnum import ConstructorsErrorEnum
import typing

class ConstructorsConstructorExploded(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

