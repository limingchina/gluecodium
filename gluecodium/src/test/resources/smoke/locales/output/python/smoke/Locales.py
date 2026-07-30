

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class Locales(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def locale_method(self, input: str) -> str:
        return _wrap(self._native.locale_method(_unwrap(input, str)), str)

    @property
    def locale_property(self) -> str:
        return _wrap(self._native.locale_property, str)

    @locale_property.setter
    def locale_property(self, value: str):
        self._native.locale_property = _unwrap(value, str)

