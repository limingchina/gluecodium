

import typing

from _native_base import _NativeBase

import generated


class Locales(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def locale_method(self, input: str) -> str: ...

    @property
    def locale_property(self) -> str:
        """"""
        return self._native.locale_property

    @locale_property.setter
    def locale_property(self, value: str):
        self._native.locale_property = value

