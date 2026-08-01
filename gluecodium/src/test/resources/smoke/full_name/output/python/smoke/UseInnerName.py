

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.OuterName import OuterName

class UseInnerName(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_foo(self) -> OuterName.InnerName:
        return _wrap(self._native.do_foo(), OuterName.InnerName)


