

import typing

from _native_base import _NativeBase

import generated


class ExternalClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_method(self, some_parameter: int): ...

    @property
    def some_property(self) -> str:
        """"""
        return _wrap(self._native.some_property, str)


