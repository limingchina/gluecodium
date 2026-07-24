

from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct
import typing

class DeclarationOrderWithFunctionsFooBar(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

