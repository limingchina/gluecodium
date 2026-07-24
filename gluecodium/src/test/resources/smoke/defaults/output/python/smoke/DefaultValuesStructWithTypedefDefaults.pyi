

import typing


from _native_base import _NativeBase

import generated


class DefaultValuesStructWithTypedefDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultValuesStructWithTypedefDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultValuesStructWithTypedefDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def long_field(self) -> int:
        """"""
        return _wrap(self._native.long_field, int)
    @long_field.setter
    def long_field(self, value: int):
      self._native.long_field = _unwrap(value, int)



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


