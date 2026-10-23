

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
from typing import Callable
import generated


@_mark_callback_base
class SpecialNamesInterface(generated.smoke_SpecialNamesInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("dispatch", "__gluecodium_callback_736d6f6b652e5370656369616c4e616d6573496e746572666163652e6469737061746368", "method", None,
             lambda: ([Callable[[], None]], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_SpecialNamesInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def dispatch(self, callback: Callable[[], None]):
        return _wrap(generated.smoke_SpecialNamesInterface.dispatch(self, _unwrap(callback, Callable[[], None])), None)

    Callback = Callable[[], None]
