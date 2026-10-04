

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.ListenerInterface import ListenerInterface

@_mark_callback_base
class Weakling(generated.smoke_Weakling):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("listener", "__gluecodium_callback_736d6f6b652e5765616b6c696e672e6c697374656e6572_get", "get", "get_listener",
             lambda: ([], Optional[ListenerInterface])),
            ("listener", "__gluecodium_callback_736d6f6b652e5765616b6c696e672e6c697374656e6572_set", "set", "set_listener",
             lambda: ([Optional[ListenerInterface]], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_Weakling):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @property
    def listener(self):
        return _wrap(generated.smoke_Weakling.listener.fget(self), Optional[ListenerInterface])

    @listener.setter
    def listener(self, value):
        generated.smoke_Weakling.listener.fset(self, _unwrap(value, Optional[ListenerInterface]))


