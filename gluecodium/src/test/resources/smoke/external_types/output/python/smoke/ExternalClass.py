

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class ExternalClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_method(self, some_parameter: int):
        """"""
        return _wrap(self._native.some_method(_unwrap(some_parameter, int)), None)

    @property
    def some_property(self) -> str:
        """"""
        return _wrap(self._native.some_property, str)


