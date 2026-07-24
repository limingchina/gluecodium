

from smoke.CppRefReturnTypeSomeStruct import CppRefReturnTypeSomeStruct
import typing

class CppRefReturnTypeStructBased(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

