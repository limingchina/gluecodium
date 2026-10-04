

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

import datetime

@_mark_callback_base
class DurationInterface(generated.smoke_DurationInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("duration_function", "__gluecodium_callback_736d6f6b652e4475726174696f6e496e746572666163652e6475726174696f6e46756e6374696f6e", "method", None,
             lambda: ([datetime.timedelta], str)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_DurationInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def duration_function(self, input: datetime.timedelta) -> str:
        return _wrap(generated.smoke_DurationInterface.duration_function(self, _unwrap(input, datetime.timedelta)), str)
