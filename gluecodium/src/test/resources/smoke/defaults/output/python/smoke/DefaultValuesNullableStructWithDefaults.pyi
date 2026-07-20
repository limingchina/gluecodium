

import typing


from _native_base import _NativeBase

import generated


class DefaultValuesNullableStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultValuesNullableStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultValuesNullableStructWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self):
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def uint_field(self):
        """"""
        return self._native.uint_field
    @uint_field.setter
    def uint_field(self, value):
      self._native.uint_field = getattr(value, "_native", value)



    @property
    def float_field(self):
        """"""
        return self._native.float_field
    @float_field.setter
    def float_field(self, value):
      self._native.float_field = getattr(value, "_native", value)



    @property
    def bool_field(self):
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value):
      self._native.bool_field = getattr(value, "_native", value)



    @property
    def string_field(self):
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value):
      self._native.string_field = getattr(value, "_native", value)


