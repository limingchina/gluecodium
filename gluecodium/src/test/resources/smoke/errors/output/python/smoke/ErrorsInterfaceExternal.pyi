

from smoke.ErrorsInterfaceExternalErrors import ErrorsInterfaceExternalErrors
import typing

class ErrorsInterfaceExternal(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

