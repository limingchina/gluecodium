

import typing


from _native_base import _NativeBase

import generated


class TypesWithDefaultsStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypesWithDefaultsStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaultsStructWithDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def uint_field(self) -> int:
        """"""
        return _wrap(self._native.uint_field, int)
    @uint_field.setter
    def uint_field(self, value: int):
      self._native.uint_field = _unwrap(value, int)



    @property
    def float_field(self) -> float:
        """"""
        return _wrap(self._native.float_field, float)
    @float_field.setter
    def float_field(self, value: float):
      self._native.float_field = _unwrap(value, float)



    @property
    def double_field(self) -> float:
        """"""
        return _wrap(self._native.double_field, float)
    @double_field.setter
    def double_field(self, value: float):
      self._native.double_field = _unwrap(value, float)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


