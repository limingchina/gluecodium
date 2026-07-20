

from smoke.NullableSomeEnum import NullableSomeEnum
from smoke.NullableSomeStruct import NullableSomeStruct
from smoke.SomeInterface import SomeInterface
import typing


from _native_base import _NativeBase

import generated


class NullableNullableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.NullableNullableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.NullableNullableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def string_field(self):
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value):
      self._native.string_field = getattr(value, "_native", value)



    @property
    def bool_field(self):
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value):
      self._native.bool_field = getattr(value, "_native", value)



    @property
    def double_field(self):
        """"""
        return self._native.double_field
    @double_field.setter
    def double_field(self, value):
      self._native.double_field = getattr(value, "_native", value)



    @property
    def struct_field(self):
        """"""
        return Optional[NullableSomeStruct](self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def enum_field(self):
        """"""
        return Optional[NullableSomeEnum](self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value):
      self._native.enum_field = getattr(value, "_native", value)



    @property
    def array_field(self):
        """"""
        return self._native.array_field
    @array_field.setter
    def array_field(self, value):
      self._native.array_field = getattr(value, "_native", value)



    @property
    def inline_array_field(self):
        """"""
        return self._native.inline_array_field
    @inline_array_field.setter
    def inline_array_field(self, value):
      self._native.inline_array_field = getattr(value, "_native", value)



    @property
    def map_field(self):
        """"""
        return self._native.map_field
    @map_field.setter
    def map_field(self, value):
      self._native.map_field = getattr(value, "_native", value)



    @property
    def instance_field(self):
        """"""
        return Optional[SomeInterface](self._native.instance_field)
    @instance_field.setter
    def instance_field(self, value):
      self._native.instance_field = getattr(value, "_native", value)


