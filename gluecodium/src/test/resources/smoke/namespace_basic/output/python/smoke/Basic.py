

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class Basic(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def basic_method(input_string: str) -> str:
        return _wrap(generated.smoke_Basic.basic_method(_unwrap(input_string, str)), str)
