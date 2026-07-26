

import typing


from _native_base import _NativeBase

import generated


class LocalesLocaleStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_LocalesLocaleStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_LocalesLocaleStruct(*[_unwrap(arg) for arg in args]))


    @property
    def locale_field(self) -> str:
        """"""
        return _wrap(self._native.locale_field, str)
    @locale_field.setter
    def locale_field(self, value: str):
      self._native.locale_field = _unwrap(value, str)


