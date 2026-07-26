

from smoke.CppRefReturnTypeEnumBased import CppRefReturnTypeEnumBased
from smoke.CppRefReturnTypeInternalError import CppRefReturnTypeInternalError
from smoke.CppRefReturnTypeSomeStruct import CppRefReturnTypeSomeStruct
from smoke.CppRefReturnTypeStructBased import CppRefReturnTypeStructBased
import typing

from _native_base import _NativeBase

import generated


class CppRefReturnType(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def void_ref(): ...

    @staticmethod
    def bool_ref() -> bool: ...

    @staticmethod
    def string_ref() -> str: ...

    @staticmethod
    def struct_ref() -> CppRefReturnTypeSomeStruct: ...

    @staticmethod
    def class_ref() -> CppRefReturnType: ...

    @staticmethod
    def nullable_ref() -> Optional[str]: ...

    @staticmethod
    def throwing_enum_with_void(): ...

    @staticmethod
    def throwing_enum_with_string() -> str: ...

    @staticmethod
    def throwing_struct_with_void(): ...

    @staticmethod
    def throwing_struct_with_string() -> str: ...


    @staticmethod
    def string_property() -> str:
        """"""
        return _wrap(generated.smoke_CppRefReturnType.string_property(), str)

