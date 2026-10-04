

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.Comments import Comments

class UnicodeComments(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input: str) -> bool:
        """Süßölgefäß"""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input, str)), bool)


