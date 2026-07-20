

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface
import typing

from _native_base import _NativeBase

import generated


class Nullable(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def method_with_string(self, input: Optional[str]) -> Optional[str]: ...

    def method_with_boolean(self, input: Optional[bool]) -> Optional[bool]: ...

    def method_with_double(self, input: Optional[float]) -> Optional[float]: ...

    def method_with_int(self, input: Optional[int]) -> Optional[int]: ...

    def method_with_some_struct(self, input: Optional[NullableSomeStruct]) -> Optional[NullableSomeStruct]: ...

    def method_with_some_enum(self, input: Optional[NullableSomeEnum]) -> Optional[NullableSomeEnum]: ...

    def method_with_some_array(self, input: Optional[list[str]]) -> Optional[list[str]]: ...

    def method_with_inline_array(self, input: Optional[list[str]]) -> Optional[list[str]]: ...

    def method_with_some_map(self, input: Optional[dict[int, str]]) -> Optional[dict[int, str]]: ...

    def method_with_instance(self, input: Optional[SomeInterface]) -> Optional[SomeInterface]: ...

    @property
    def string_property(self):
        """"""
        return self._native.string_property

    @string_property.setter
    def string_property(self, value):
        self._native.string_property = value

    @property
    def is_bool_property(self):
        """"""
        return self._native.is_bool_property

    @is_bool_property.setter
    def is_bool_property(self, value):
        self._native.is_bool_property = value

    @property
    def double_property(self):
        """"""
        return self._native.double_property

    @double_property.setter
    def double_property(self, value):
        self._native.double_property = value

    @property
    def int_property(self):
        """"""
        return self._native.int_property

    @int_property.setter
    def int_property(self, value):
        self._native.int_property = value

    @property
    def struct_property(self):
        """"""
        return self._native.struct_property

    @struct_property.setter
    def struct_property(self, value):
        self._native.struct_property = value

    @property
    def enum_property(self):
        """"""
        return self._native.enum_property

    @enum_property.setter
    def enum_property(self, value):
        self._native.enum_property = value

    @property
    def array_property(self):
        """"""
        return self._native.array_property

    @array_property.setter
    def array_property(self, value):
        self._native.array_property = value

    @property
    def inline_array_property(self):
        """"""
        return self._native.inline_array_property

    @inline_array_property.setter
    def inline_array_property(self, value):
        self._native.inline_array_property = value

    @property
    def map_property(self):
        """"""
        return self._native.map_property

    @map_property.setter
    def map_property(self, value):
        self._native.map_property = value

    @property
    def instance_property(self):
        """"""
        return self._native.instance_property

    @instance_property.setter
    def instance_property(self, value):
        self._native.instance_property = value

