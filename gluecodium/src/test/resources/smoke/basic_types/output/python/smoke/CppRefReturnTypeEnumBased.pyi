

from smoke.CppRefReturnTypeInternalError import CppRefReturnTypeInternalError
import typing

class CppRefReturnTypeEnumBased(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

