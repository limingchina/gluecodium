

import typing

from _native_base import _NativeBase

import generated


class AttributesClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def very_fun(self, param: str): ...

    @property
    def prop(self) -> str:
        """"""
        return _wrap(self._native.prop, str)

    @prop.setter
    def prop(self, value: str):
        self._native.prop = _unwrap(value, str)


    PI = False

