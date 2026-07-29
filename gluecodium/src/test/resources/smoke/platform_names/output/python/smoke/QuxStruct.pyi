

import typing


from _native_base import _NativeBase

import generated


class QuxStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_QuxStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_QuxStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def qux_field(self) -> str:
        """"""
        return _wrap(self._native.qux_field, str)
    @qux_field.setter
    def qux_field(self, value: str):
      self._native.qux_field = _unwrap(value, str)


    @staticmethod
    def qux_make(qux_parameter: str) -> QuxStruct: ...

