

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class SomeCoolClassType(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_important_stuff(self):
        return _wrap(self._native.do_important_stuff(), None)

