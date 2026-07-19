

from __future__ import annotations

from smoke.EnumsErrorStruct import EnumsErrorStruct
from smoke.EnumsInternalErrorCode import EnumsInternalErrorCode
from smoke.EnumsSimpleEnum import EnumsSimpleEnum

from _native_base import _NativeBase

import generated


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_enumeration(input: EnumsSimpleEnum) -> EnumsSimpleEnum:
        """"""
        native_result = generated.Enums.method_with_enumeration(input._native)
        return EnumsSimpleEnum(native_result)

    @staticmethod
    def flip_enum_value(input: EnumsInternalErrorCode) -> EnumsInternalErrorCode:
        """"""
        native_result = generated.Enums.flip_enum_value(input._native)
        return EnumsInternalErrorCode(native_result)

    @staticmethod
    def extract_enum_from_struct(input: EnumsErrorStruct) -> EnumsInternalErrorCode:
        """"""
        native_result = generated.Enums.extract_enum_from_struct(input._native)
        return EnumsInternalErrorCode(native_result)

    @staticmethod
    def create_struct_with_enum_inside(type: EnumsInternalErrorCode, message: str) -> EnumsErrorStruct:
        """"""
        native_result = generated.Enums.create_struct_with_enum_inside(type._native, message)
        return EnumsErrorStruct(native_result)

