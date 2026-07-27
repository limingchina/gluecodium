

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface
import typing


from _native_base import _NativeBase

import generated


class NullableNullableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_NullableNullableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_NullableNullableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def string_field(self):
        """"""
        return _wrap(self._native.string_field, Optional[str])
    @string_field.setter
    def string_field(self, value):
      self._native.string_field = _unwrap(value, Optional[str])



    @property
    def bool_field(self):
        """"""
        return _wrap(self._native.bool_field, Optional[bool])
    @bool_field.setter
    def bool_field(self, value):
      self._native.bool_field = _unwrap(value, Optional[bool])



    @property
    def double_field(self):
        """"""
        return _wrap(self._native.double_field, Optional[float])
    @double_field.setter
    def double_field(self, value):
      self._native.double_field = _unwrap(value, Optional[float])



    @property
    def struct_field(self):
        """"""
        return _wrap(self._native.struct_field, Optional[NullableSomeStruct])
    @struct_field.setter
    def struct_field(self, value):
      self._native.struct_field = _unwrap(value, Optional[NullableSomeStruct])



    @property
    def enum_field(self):
        """"""
        return _wrap(self._native.enum_field, Optional[NullableSomeEnum])
    @enum_field.setter
    def enum_field(self, value):
      self._native.enum_field = _unwrap(value, Optional[NullableSomeEnum])



    @property
    def array_field(self):
        """"""
        return _wrap(self._native.array_field, Optional[list[str]])
    @array_field.setter
    def array_field(self, value):
      self._native.array_field = _unwrap(value, Optional[list[str]])



    @property
    def inline_array_field(self):
        """"""
        return _wrap(self._native.inline_array_field, Optional[list[str]])
    @inline_array_field.setter
    def inline_array_field(self, value):
      self._native.inline_array_field = _unwrap(value, Optional[list[str]])



    @property
    def map_field(self):
        """"""
        return _wrap(self._native.map_field, Optional[dict[int, str]])
    @map_field.setter
    def map_field(self, value):
      self._native.map_field = _unwrap(value, Optional[dict[int, str]])



    @property
    def instance_field(self):
        """"""
        return _wrap(self._native.instance_field, Optional[SomeInterface])
    @instance_field.setter
    def instance_field(self, value):
      self._native.instance_field = _unwrap(value, Optional[SomeInterface])


