

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

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
        native_result = generated.smoke_Enums.method_with_enumeration(_unwrap(input, EnumsSimpleEnum))
        return _get_or_create_wrapper(native_result, EnumsSimpleEnum)

    @staticmethod
    def flip_enum_value(input: EnumsInternalErrorCode) -> EnumsInternalErrorCode:
        """"""
        native_result = generated.smoke_Enums.flip_enum_value(_unwrap(input, EnumsInternalErrorCode))
        return _get_or_create_wrapper(native_result, EnumsInternalErrorCode)

    @staticmethod
    def extract_enum_from_struct(input: EnumsErrorStruct) -> EnumsInternalErrorCode:
        """"""
        native_result = generated.smoke_Enums.extract_enum_from_struct(_unwrap(input, EnumsErrorStruct))
        return _get_or_create_wrapper(native_result, EnumsInternalErrorCode)

    @staticmethod
    def create_struct_with_enum_inside(type: EnumsInternalErrorCode, message: str) -> EnumsErrorStruct:
        """"""
        native_result = generated.smoke_Enums.create_struct_with_enum_inside(_unwrap(type, EnumsInternalErrorCode), _unwrap(message, str))
        return _get_or_create_wrapper(native_result, EnumsErrorStruct)

