

from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum
import typing

class ExternalClassConstructorExploded(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

