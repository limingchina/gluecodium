

import typing


from _native_base import _NativeBase

import generated


class SomeMutableCustomStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SomeMutableCustomStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SomeMutableCustomStructWithDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def list_field(self) -> list[int]:
        """"""
        return _wrap(self._native.list_field, list[int])
    @list_field.setter
    def list_field(self, value: list[int]):
      self._native.list_field = _unwrap(value, list[int])


