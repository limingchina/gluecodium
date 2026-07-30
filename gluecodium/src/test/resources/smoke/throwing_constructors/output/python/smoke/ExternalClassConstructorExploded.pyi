

from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum
import typing

class ExternalClassConstructorExploded(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

