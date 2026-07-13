

from __future__ import annotations

from smoke.EnumBasedError import EnumBasedError
from smoke.InternalError import InternalError
from smoke.SomeStruct import SomeStruct
from smoke.StructBasedError import StructBasedError


from _native_base import _NativeBase

import generated


class CppRefReturnType(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def void_ref():
        """"""
        native_result = generated.CppRefReturnType.void_ref()
        return None(native_result)

    @staticmethod

    def bool_ref() -> bool:
        """"""
        native_result = generated.CppRefReturnType.bool_ref()
        return bool(native_result)

    @staticmethod

    def string_ref() -> str:
        """"""
        native_result = generated.CppRefReturnType.string_ref()
        return str(native_result)

    @staticmethod

    def struct_ref() -> SomeStruct:
        """"""
        native_result = generated.CppRefReturnType.struct_ref()
        return SomeStruct(native_result)

    @staticmethod

    def class_ref() -> CppRefReturnType:
        """"""
        native_result = generated.CppRefReturnType.class_ref()
        return CppRefReturnType(native_result)

    @staticmethod

    def nullable_ref() -> Optional[str]:
        """"""
        native_result = generated.CppRefReturnType.nullable_ref()
        return Optional[str](native_result)

    @staticmethod

    def throwing_enum_with_void():
        """"""
        native_result = generated.CppRefReturnType.throwing_enum_with_void()
        return None(native_result)

    @staticmethod

    def throwing_enum_with_string() -> str:
        """"""
        native_result = generated.CppRefReturnType.throwing_enum_with_string()
        return str(native_result)

    @staticmethod

    def throwing_struct_with_void():
        """"""
        native_result = generated.CppRefReturnType.throwing_struct_with_void()
        return None(native_result)

    @staticmethod

    def throwing_struct_with_string() -> str:
        """"""
        native_result = generated.CppRefReturnType.throwing_struct_with_string()
        return str(native_result)


    @property
    def string_property(self) -> str:
        """"""
        return self._native.string_property


from enum import Enum


class InternalError(Enum):
    """"""

    FOO = 0
    BAR = 1

