

from __future__ import annotations

from smoke.ErrorStruct import ErrorStruct
from smoke.InternalErrorCode import InternalErrorCode
from smoke.SimpleEnum import SimpleEnum


from _native_base import _NativeBase

import generated


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def method_with_enumeration(input: SimpleEnum) -> SimpleEnum:
        """"""
        native_result = generated.Enums.method_with_enumeration(input)
        return SimpleEnum(native_result)

    @staticmethod

    def flip_enum_value(input: InternalErrorCode) -> InternalErrorCode:
        """"""
        native_result = generated.Enums.flip_enum_value(input)
        return InternalErrorCode(native_result)

    @staticmethod

    def extract_enum_from_struct(input: ErrorStruct) -> InternalErrorCode:
        """"""
        native_result = generated.Enums.extract_enum_from_struct(input)
        return InternalErrorCode(native_result)

    @staticmethod

    def create_struct_with_enum_inside(type: InternalErrorCode, message: str) -> ErrorStruct:
        """"""
        native_result = generated.Enums.create_struct_with_enum_inside(type, message)
        return ErrorStruct(native_result)

