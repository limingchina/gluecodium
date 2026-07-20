

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DefaultValuesStructWithSpecialDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultValuesStructWithSpecialDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultValuesStructWithSpecialDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def float_nan_field(self) -> float:
        """"""
        return self._native.float_nan_field
    @float_nan_field.setter
    def float_nan_field(self, value: float):
      self._native.float_nan_field = getattr(value, "_native", value)



    @property
    def float_infinity_field(self) -> float:
        """"""
        return self._native.float_infinity_field
    @float_infinity_field.setter
    def float_infinity_field(self, value: float):
      self._native.float_infinity_field = getattr(value, "_native", value)



    @property
    def float_negative_infinity_field(self) -> float:
        """"""
        return self._native.float_negative_infinity_field
    @float_negative_infinity_field.setter
    def float_negative_infinity_field(self, value: float):
      self._native.float_negative_infinity_field = getattr(value, "_native", value)



    @property
    def double_nan_field(self) -> float:
        """"""
        return self._native.double_nan_field
    @double_nan_field.setter
    def double_nan_field(self, value: float):
      self._native.double_nan_field = getattr(value, "_native", value)



    @property
    def double_infinity_field(self) -> float:
        """"""
        return self._native.double_infinity_field
    @double_infinity_field.setter
    def double_infinity_field(self, value: float):
      self._native.double_infinity_field = getattr(value, "_native", value)



    @property
    def double_negative_infinity_field(self) -> float:
        """"""
        return self._native.double_negative_infinity_field
    @double_negative_infinity_field.setter
    def double_negative_infinity_field(self, value: float):
      self._native.double_negative_infinity_field = getattr(value, "_native", value)


