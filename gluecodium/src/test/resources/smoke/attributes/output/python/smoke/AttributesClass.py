

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class AttributesClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def very_fun(self, param: str):
        """"""
        return _wrap(self._native.very_fun(_unwrap(param, str)), None)

    @property
    def prop(self) -> str:
        """"""
        return _wrap(self._native.prop, str)

    @prop.setter
    def prop(self, value: str):
        self._native.prop = _unwrap(value, str)


    PI = False

