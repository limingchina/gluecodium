

from smoke.ErrorsInterfaceInternalError import ErrorsInterfaceInternalError
import typing

class ErrorsInterfaceInternal(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

