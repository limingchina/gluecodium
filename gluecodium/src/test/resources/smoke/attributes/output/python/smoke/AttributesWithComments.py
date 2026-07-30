

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class AttributesWithComments(_NativeBase):
    """Class comment"""
    def __init__(self, native):
        super().__init__(native)

    def very_fun(self):
        """Function comment"""
        return _wrap(self._native.very_fun(), None)

    @property
    def prop(self) -> str:
        """Property comment"""
        return _wrap(self._native.prop, str)

    @prop.setter
    def prop(self, value: str):
        """Setter comment"""
        self._native.prop = _unwrap(value, str)

    #: Const comment
    PI = False

