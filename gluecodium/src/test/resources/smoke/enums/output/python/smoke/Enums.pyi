

from smoke.ErrorStruct import ErrorStruct
from smoke.InternalErrorCode import InternalErrorCode
from smoke.SimpleEnum import SimpleEnum

from _native_base import _NativeBase


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_enumeration(self, input: SimpleEnum) -> SimpleEnum:
        """"""
        return self._native.method_with_enumeration(input)


    def flip_enum_value(self, input: InternalErrorCode) -> InternalErrorCode:
        """"""
        return self._native.flip_enum_value(input)


    def extract_enum_from_struct(self, input: ErrorStruct) -> InternalErrorCode:
        """"""
        return self._native.extract_enum_from_struct(input)


    def create_struct_with_enum_inside(self, type: InternalErrorCode, message: str) -> ErrorStruct:
        """"""
        return self._native.create_struct_with_enum_inside(type, message)

