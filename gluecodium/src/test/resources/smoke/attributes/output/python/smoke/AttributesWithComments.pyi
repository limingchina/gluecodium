

import typing

from _native_base import _NativeBase

import generated


class AttributesWithComments(_NativeBase):
    """Class comment"""

    def __init__(self, native):
        super().__init__(native)

    def very_fun(self): ...

    @property
    def prop(self) -> str:
        """Property comment"""
        return _wrap(self._native.prop, str)

    @prop.setter
    def prop(self, value: str):
        self._native.prop = _unwrap(value, str)

    Const comment
    PI = False

