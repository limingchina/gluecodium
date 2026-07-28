

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class SpecialNames(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def create(self):
        """"""
        return _wrap(self._native.create(), None)

    def release(self):
        """"""
        return _wrap(self._native.release(), None)

    def create_proxy(self):
        """"""
        return _wrap(self._native.create_proxy(), None)

    def _uppercase(self):
        """"""
        return _wrap(self._native._uppercase(), None)

    @staticmethod
    def make(result: str) -> SpecialNames:
        """"""
        native_result = generated.smoke_SpecialNames.make(_unwrap(result, str))
        return _get_or_create_wrapper(native_result, SpecialNames)

