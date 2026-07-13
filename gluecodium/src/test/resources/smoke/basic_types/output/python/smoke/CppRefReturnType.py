

from smoke.CppRefReturnType import CppRefReturnType
from smoke.EnumBasedError import EnumBasedError
from smoke.InternalError import InternalError
from smoke.SomeStruct import SomeStruct
from smoke.StructBasedError import StructBasedError

class CppRefReturnType:
    """"""

    def __init__(self, native):
        self._native = native


    def void_ref(self):
        """"""
        return self._native.void_ref()


    def bool_ref(self) -> bool:
        """"""
        return self._native.bool_ref()


    def string_ref(self) -> str:
        """"""
        return self._native.string_ref()


    def struct_ref(self) -> SomeStruct:
        """"""
        return self._native.struct_ref()


    def class_ref(self) -> CppRefReturnType:
        """"""
        return self._native.class_ref()


    def nullable_ref(self) -> Optional[str]:
        """"""
        return self._native.nullable_ref()


    def throwing_enum_with_void(self):
        """"""
        return self._native.throwing_enum_with_void()


    def throwing_enum_with_string(self) -> str:
        """"""
        return self._native.throwing_enum_with_string()


    def throwing_struct_with_void(self):
        """"""
        return self._native.throwing_struct_with_void()


    def throwing_struct_with_string(self) -> str:
        """"""
        return self._native.throwing_struct_with_string()


    @property
    def string_property(self) -> str:
        """"""
        return self._native.string_property


