

from smoke.ErrorsInterfaceExternalErrors import ErrorsInterfaceExternalErrors
import typing

class ErrorsInterfaceExternal(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

