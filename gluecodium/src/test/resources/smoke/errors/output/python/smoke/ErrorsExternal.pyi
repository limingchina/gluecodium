

from smoke.ErrorsExternalErrors import ErrorsExternalErrors
import typing

class ErrorsExternal(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

