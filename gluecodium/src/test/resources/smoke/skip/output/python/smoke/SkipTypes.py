

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.SkipTypesNotInDart import SkipTypesNotInDart

from _native_base import _NativeBase

import generated


class SkipTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def use_list_in_dart(self) -> list[SkipTypesNotInDart]:
        """"""
        return _wrap(self._native.use_list_in_dart(), list[SkipTypesNotInDart])

