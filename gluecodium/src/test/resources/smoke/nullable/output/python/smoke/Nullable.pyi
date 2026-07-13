

from smoke.SomeEnum import SomeEnum
from smoke.SomeInterface import SomeInterface
from smoke.SomeStruct import SomeStruct
from smoke.dict[int, str] import dict[int, str]
from smoke.list[str] import list[str]

from _native_base import _NativeBase


class Nullable(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_string(self, input: Optional[str]) -> Optional[str]:
        """"""
        return self._native.method_with_string(input)


    def method_with_boolean(self, input: Optional[bool]) -> Optional[bool]:
        """"""
        return self._native.method_with_boolean(input)


    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        """"""
        return self._native.method_with_double(input)


    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_int(input)


    def method_with_some_struct(self, input: Optional[SomeStruct]) -> Optional[SomeStruct]:
        """"""
        return self._native.method_with_some_struct(input)


    def method_with_some_enum(self, input: Optional[SomeEnum]) -> Optional[SomeEnum]:
        """"""
        return self._native.method_with_some_enum(input)


    def method_with_some_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        """"""
        return self._native.method_with_some_array(input)


    def method_with_inline_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        """"""
        return self._native.method_with_inline_array(input)


    def method_with_some_map(self, input: Optional[dict[int, str]]) -> Optional[dict[int, str]]:
        """"""
        return self._native.method_with_some_map(input)


    def method_with_instance(self, input: Optional[SomeInterface]) -> Optional[SomeInterface]:
        """"""
        return self._native.method_with_instance(input)


    @property
    def string_property(self):
        """"""
        return self._native.string_property



    @property
    def is_bool_property(self):
        """"""
        return self._native.is_bool_property



    @property
    def double_property(self):
        """"""
        return self._native.double_property



    @property
    def int_property(self):
        """"""
        return self._native.int_property



    @property
    def struct_property(self):
        """"""
        return self._native.struct_property



    @property
    def enum_property(self):
        """"""
        return self._native.enum_property



    @property
    def array_property(self):
        """"""
        return self._native.array_property



    @property
    def inline_array_property(self):
        """"""
        return self._native.inline_array_property



    @property
    def map_property(self):
        """"""
        return self._native.map_property



    @property
    def instance_property(self):
        """"""
        return self._native.instance_property


