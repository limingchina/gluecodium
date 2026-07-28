

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class MultipleAttributesSwift(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def no_lists2(self):
        """"""
        return _wrap(self._native.no_lists2(), None)

    def no_lists3(self):
        """"""
        return _wrap(self._native.no_lists3(), None)

    def list_first(self):
        """"""
        return _wrap(self._native.list_first(), None)

    def list_second(self):
        """"""
        return _wrap(self._native.list_second(), None)

    def two_lists(self):
        """"""
        return _wrap(self._native.two_lists(), None)

