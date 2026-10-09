

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.Rectangle import Rectangle

class ExternalDartConstants(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalDartConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalDartConstants(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    SMALL = Rectangle(0, 0, 1, 1)

    BIG = Rectangle(0, 0, 10, 10)
