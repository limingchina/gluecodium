

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.CppRefReturnTypeEnumBased import CppRefReturnTypeEnumBased
from smoke.CppRefReturnTypeInternalError import CppRefReturnTypeInternalError
from smoke.CppRefReturnTypeSomeStruct import CppRefReturnTypeSomeStruct
from smoke.CppRefReturnTypeStructBased import CppRefReturnTypeStructBased

from _native_base import _NativeBase

import generated


class CppRefReturnType(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def void_ref():
        """"""
        generated.smoke_CppRefReturnType.void_ref()

    @staticmethod
    def bool_ref() -> bool:
        """"""
        return generated.smoke_CppRefReturnType.bool_ref()

    @staticmethod
    def string_ref() -> str:
        """"""
        return generated.smoke_CppRefReturnType.string_ref()

    @staticmethod
    def struct_ref() -> CppRefReturnTypeSomeStruct:
        """"""
        native_result = generated.smoke_CppRefReturnType.struct_ref()
        return CppRefReturnTypeSomeStruct(native_result)

    @staticmethod
    def class_ref() -> CppRefReturnType:
        """"""
        native_result = generated.smoke_CppRefReturnType.class_ref()
        return CppRefReturnType(native_result)

    @staticmethod
    def nullable_ref() -> Optional[str]:
        """"""
        return generated.smoke_CppRefReturnType.nullable_ref()

    @staticmethod
    def throwing_enum_with_void():
        """"""
        generated.smoke_CppRefReturnType.throwing_enum_with_void()

    @staticmethod
    def throwing_enum_with_string() -> str:
        """"""
        return generated.smoke_CppRefReturnType.throwing_enum_with_string()

    @staticmethod
    def throwing_struct_with_void():
        """"""
        generated.smoke_CppRefReturnType.throwing_struct_with_void()

    @staticmethod
    def throwing_struct_with_string() -> str:
        """"""
        return generated.smoke_CppRefReturnType.throwing_struct_with_string()


    @staticmethod
    def string_property() -> str:
        """"""
        return _wrap(generated.smoke_CppRefReturnType.string_property(), str)

