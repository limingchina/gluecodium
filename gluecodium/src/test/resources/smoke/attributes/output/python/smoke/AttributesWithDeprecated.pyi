

import typing

from _native_base import _NativeBase

import generated


class AttributesWithDeprecated(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def very_fun(self): ...

    @property
    def prop(self) -> str:
        """"""
        return self._native.prop

    @prop.setter
    def prop(self, value: str):
        self._native.prop = value


    PI = False

