

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.SomeTypeCollection import SomeTypeCollection

class UseTcException(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        return _wrap(self._native.do_nothing(), None)


