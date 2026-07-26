

import typing


from _native_base import _NativeBase

import generated


class DefaultValuesStructWithSpecialDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_DefaultValuesStructWithSpecialDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DefaultValuesStructWithSpecialDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def float_nan_field(self) -> float:
        """"""
        return _wrap(self._native.float_nan_field, float)
    @float_nan_field.setter
    def float_nan_field(self, value: float):
      self._native.float_nan_field = _unwrap(value, float)



    @property
    def float_infinity_field(self) -> float:
        """"""
        return _wrap(self._native.float_infinity_field, float)
    @float_infinity_field.setter
    def float_infinity_field(self, value: float):
      self._native.float_infinity_field = _unwrap(value, float)



    @property
    def float_negative_infinity_field(self) -> float:
        """"""
        return _wrap(self._native.float_negative_infinity_field, float)
    @float_negative_infinity_field.setter
    def float_negative_infinity_field(self, value: float):
      self._native.float_negative_infinity_field = _unwrap(value, float)



    @property
    def double_nan_field(self) -> float:
        """"""
        return _wrap(self._native.double_nan_field, float)
    @double_nan_field.setter
    def double_nan_field(self, value: float):
      self._native.double_nan_field = _unwrap(value, float)



    @property
    def double_infinity_field(self) -> float:
        """"""
        return _wrap(self._native.double_infinity_field, float)
    @double_infinity_field.setter
    def double_infinity_field(self, value: float):
      self._native.double_infinity_field = _unwrap(value, float)



    @property
    def double_negative_infinity_field(self) -> float:
        """"""
        return _wrap(self._native.double_negative_infinity_field, float)
    @double_negative_infinity_field.setter
    def double_negative_infinity_field(self, value: float):
      self._native.double_negative_infinity_field = _unwrap(value, float)


