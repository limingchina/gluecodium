

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface

from _native_base import _NativeBase

import generated


class Nullable(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def method_with_string(self, input: Optional[str]) -> Optional[str]:
        """"""
        return _wrap(self._native.method_with_string(_unwrap(input, Optional[str])), Optional[str])

    def method_with_boolean(self, input: Optional[bool]) -> Optional[bool]:
        """"""
        return _wrap(self._native.method_with_boolean(_unwrap(input, Optional[bool])), Optional[bool])

    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        """"""
        return _wrap(self._native.method_with_double(_unwrap(input, Optional[float])), Optional[float])

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return _wrap(self._native.method_with_int(_unwrap(input, Optional[int])), Optional[int])

    def method_with_some_struct(self, input: Optional[NullableSomeStruct]) -> Optional[NullableSomeStruct]:
        """"""
        return _wrap(self._native.method_with_some_struct(_unwrap(input, Optional[NullableSomeStruct])), Optional[NullableSomeStruct])

    def method_with_some_enum(self, input: Optional[NullableSomeEnum]) -> Optional[NullableSomeEnum]:
        """"""
        return _wrap(self._native.method_with_some_enum(_unwrap(input, Optional[NullableSomeEnum])), Optional[NullableSomeEnum])

    def method_with_some_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        """"""
        return _wrap(self._native.method_with_some_array(_unwrap(input, Optional[list[str]])), Optional[list[str]])

    def method_with_inline_array(self, input: Optional[list[str]]) -> Optional[list[str]]:
        """"""
        return _wrap(self._native.method_with_inline_array(_unwrap(input, Optional[list[str]])), Optional[list[str]])

    def method_with_some_map(self, input: Optional[dict[int, str]]) -> Optional[dict[int, str]]:
        """"""
        return _wrap(self._native.method_with_some_map(_unwrap(input, Optional[dict[int, str]])), Optional[dict[int, str]])

    def method_with_instance(self, input: Optional[SomeInterface]) -> Optional[SomeInterface]:
        """"""
        return _wrap(self._native.method_with_instance(_unwrap(input, Optional[SomeInterface])), Optional[SomeInterface])

    @property
    def string_property(self):
        """"""
        return _wrap(self._native.string_property, Optional[str])

    @string_property.setter
    def string_property(self, value):
        self._native.string_property = _unwrap(value, Optional[str])

    @property
    def is_bool_property(self):
        """"""
        return _wrap(self._native.is_bool_property, Optional[bool])

    @is_bool_property.setter
    def is_bool_property(self, value):
        self._native.is_bool_property = _unwrap(value, Optional[bool])

    @property
    def double_property(self):
        """"""
        return _wrap(self._native.double_property, Optional[float])

    @double_property.setter
    def double_property(self, value):
        self._native.double_property = _unwrap(value, Optional[float])

    @property
    def int_property(self):
        """"""
        return _wrap(self._native.int_property, Optional[int])

    @int_property.setter
    def int_property(self, value):
        self._native.int_property = _unwrap(value, Optional[int])

    @property
    def struct_property(self):
        """"""
        return _wrap(self._native.struct_property, Optional[NullableSomeStruct])

    @struct_property.setter
    def struct_property(self, value):
        self._native.struct_property = _unwrap(value, Optional[NullableSomeStruct])

    @property
    def enum_property(self):
        """"""
        return _wrap(self._native.enum_property, Optional[NullableSomeEnum])

    @enum_property.setter
    def enum_property(self, value):
        self._native.enum_property = _unwrap(value, Optional[NullableSomeEnum])

    @property
    def array_property(self):
        """"""
        return _wrap(self._native.array_property, Optional[list[str]])

    @array_property.setter
    def array_property(self, value):
        self._native.array_property = _unwrap(value, Optional[list[str]])

    @property
    def inline_array_property(self):
        """"""
        return _wrap(self._native.inline_array_property, Optional[list[str]])

    @inline_array_property.setter
    def inline_array_property(self, value):
        self._native.inline_array_property = _unwrap(value, Optional[list[str]])

    @property
    def map_property(self):
        """"""
        return _wrap(self._native.map_property, Optional[dict[int, str]])

    @map_property.setter
    def map_property(self, value):
        self._native.map_property = _unwrap(value, Optional[dict[int, str]])

    @property
    def instance_property(self):
        """"""
        return _wrap(self._native.instance_property, Optional[SomeInterface])

    @instance_property.setter
    def instance_property(self, value):
        self._native.instance_property = _unwrap(value, Optional[SomeInterface])

