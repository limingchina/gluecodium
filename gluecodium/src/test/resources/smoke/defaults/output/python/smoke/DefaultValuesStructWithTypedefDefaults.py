

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DefaultValuesStructWithTypedefDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultValuesStructWithTypedefDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultValuesStructWithTypedefDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def long_field(self) -> int:
        """"""
        return self._native.long_field
    @long_field.setter
    def long_field(self, value: int):
      self._native.long_field = getattr(value, "_native", value)



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


