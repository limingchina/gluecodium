

from smoke.ErrorsInterfaceInternalError import ErrorsInterfaceInternalError
import typing

class ErrorsInterfaceInternal(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

