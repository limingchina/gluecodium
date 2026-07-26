

from smoke.EquatableNestedEquatableStruct import EquatableNestedEquatableStruct
from smoke.EquatableSomeEnum import EquatableSomeEnum
import typing


from _native_base import _NativeBase

import generated


class EquatableEquatableNullableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_EquatableEquatableNullableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EquatableEquatableNullableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def bool_field(self):
        """"""
        return _wrap(self._native.bool_field, Optional[bool])
    @bool_field.setter
    def bool_field(self, value):
      self._native.bool_field = _unwrap(value, Optional[bool])



    @property
    def int_field(self):
        """"""
        return _wrap(self._native.int_field, Optional[int])
    @int_field.setter
    def int_field(self, value):
      self._native.int_field = _unwrap(value, Optional[int])



    @property
    def uint_field(self):
        """"""
        return _wrap(self._native.uint_field, Optional[int])
    @uint_field.setter
    def uint_field(self, value):
      self._native.uint_field = _unwrap(value, Optional[int])



    @property
    def float_field(self):
        """"""
        return _wrap(self._native.float_field, Optional[float])
    @float_field.setter
    def float_field(self, value):
      self._native.float_field = _unwrap(value, Optional[float])



    @property
    def string_field(self):
        """"""
        return _wrap(self._native.string_field, Optional[str])
    @string_field.setter
    def string_field(self, value):
      self._native.string_field = _unwrap(value, Optional[str])



    @property
    def struct_field(self):
        """"""
        return _wrap(self._native.struct_field, Optional[EquatableNestedEquatableStruct])
    @struct_field.setter
    def struct_field(self, value):
      self._native.struct_field = _unwrap(value, Optional[EquatableNestedEquatableStruct])



    @property
    def enum_field(self):
        """"""
        return _wrap(self._native.enum_field, Optional[EquatableSomeEnum])
    @enum_field.setter
    def enum_field(self, value):
      self._native.enum_field = _unwrap(value, Optional[EquatableSomeEnum])



    @property
    def array_field(self):
        """"""
        return _wrap(self._native.array_field, Optional[list[str]])
    @array_field.setter
    def array_field(self, value):
      self._native.array_field = _unwrap(value, Optional[list[str]])



    @property
    def map_field(self):
        """"""
        return _wrap(self._native.map_field, Optional[dict[int, str]])
    @map_field.setter
    def map_field(self, value):
      self._native.map_field = _unwrap(value, Optional[dict[int, str]])


