

from smoke.CppRefReturnTypeSomeStruct import CppRefReturnTypeSomeStruct
import typing

class CppRefReturnTypeStructBased(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

