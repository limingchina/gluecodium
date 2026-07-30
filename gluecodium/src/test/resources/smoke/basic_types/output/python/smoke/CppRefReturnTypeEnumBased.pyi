

from smoke.CppRefReturnTypeInternalError import CppRefReturnTypeInternalError
import typing

class CppRefReturnTypeEnumBased(Exception):
    message: str

    def __init__(self, message: str) -> None: ...

