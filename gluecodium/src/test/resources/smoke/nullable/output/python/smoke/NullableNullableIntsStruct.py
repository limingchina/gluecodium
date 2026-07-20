

from __future__ import annotations



from _native_base import _NativeBase

import generated


class NullableNullableIntsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.NullableNullableIntsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.NullableNullableIntsStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int8_field(self):
        """"""
        return self._native.int8_field
    @int8_field.setter
    def int8_field(self, value):
      self._native.int8_field = getattr(value, "_native", value)



    @property
    def int16_field(self):
        """"""
        return self._native.int16_field
    @int16_field.setter
    def int16_field(self, value):
      self._native.int16_field = getattr(value, "_native", value)



    @property
    def int32_field(self):
        """"""
        return self._native.int32_field
    @int32_field.setter
    def int32_field(self, value):
      self._native.int32_field = getattr(value, "_native", value)



    @property
    def int64_field(self):
        """"""
        return self._native.int64_field
    @int64_field.setter
    def int64_field(self, value):
      self._native.int64_field = getattr(value, "_native", value)



    @property
    def uint8_field(self):
        """"""
        return self._native.uint8_field
    @uint8_field.setter
    def uint8_field(self, value):
      self._native.uint8_field = getattr(value, "_native", value)



    @property
    def uint16_field(self):
        """"""
        return self._native.uint16_field
    @uint16_field.setter
    def uint16_field(self, value):
      self._native.uint16_field = getattr(value, "_native", value)



    @property
    def uint32_field(self):
        """"""
        return self._native.uint32_field
    @uint32_field.setter
    def uint32_field(self, value):
      self._native.uint32_field = getattr(value, "_native", value)



    @property
    def uint64_field(self):
        """"""
        return self._native.uint64_field
    @uint64_field.setter
    def uint64_field(self, value):
      self._native.uint64_field = getattr(value, "_native", value)


