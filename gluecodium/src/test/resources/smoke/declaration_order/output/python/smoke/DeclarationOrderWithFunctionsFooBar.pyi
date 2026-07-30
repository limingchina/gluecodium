

from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct
import typing

class DeclarationOrderWithFunctionsFooBar(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

