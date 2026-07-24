

import typing


from _native_base import _NativeBase

import generated


class OuterNameInnerName(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterNameInnerName):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterNameInnerName(*[_unwrap(arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


