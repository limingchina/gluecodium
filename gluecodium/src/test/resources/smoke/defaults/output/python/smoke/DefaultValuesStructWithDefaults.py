

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DefaultValuesStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultValuesStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultValuesStructWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def uint_field(self) -> int:
        """"""
        return self._native.uint_field
    @uint_field.setter
    def uint_field(self, value: int):
      self._native.uint_field = getattr(value, "_native", value)



    @property
    def float_field(self) -> float:
        """"""
        return self._native.float_field
    @float_field.setter
    def float_field(self, value: float):
      self._native.float_field = getattr(value, "_native", value)



    @property
    def double_field(self) -> float:
        """"""
        return self._native.double_field
    @double_field.setter
    def double_field(self, value: float):
      self._native.double_field = getattr(value, "_native", value)



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)


