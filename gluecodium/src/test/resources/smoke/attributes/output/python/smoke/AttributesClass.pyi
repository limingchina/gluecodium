

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
        return self._native.prop

    @prop.setter
    def prop(self, value: str):
        self._native.prop = value


    PI = False

