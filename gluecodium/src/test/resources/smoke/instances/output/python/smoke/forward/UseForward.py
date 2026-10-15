

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.SimpleClass import SimpleClass
from smoke.SimpleInterface import SimpleInterface
from smoke.forward.Class1 import Class1
from smoke.forward.Class2 import Class2

@_mark_callback_base
class UseForward(generated.smoke_forward_UseForward):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("use_it", "__gluecodium_callback_736d6f6b652e666f72776172642e557365466f72776172642e7573655f6974", "method", None,
             lambda: ([Class1, Class2, SimpleClass, SimpleInterface], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_forward_UseForward):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def use_it(self, param1: Class1, param2: Class2, simple_class: SimpleClass, simple_interface: SimpleInterface):
        return _wrap(generated.smoke_forward_UseForward.use_it(self, _unwrap(param1, Class1), _unwrap(param2, Class2), _unwrap(simple_class, SimpleClass), _unwrap(simple_interface, SimpleInterface)), None)
