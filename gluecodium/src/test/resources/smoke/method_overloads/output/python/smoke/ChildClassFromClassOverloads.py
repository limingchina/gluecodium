

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentClass import ParentClass

@_mark_callback_base
class ChildClassFromClassOverloads(generated.smoke_ChildClassFromClassOverloads):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("foo", "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173734f7665726c6f6164732e666f6f", "method", None,
             lambda: ([str], None)),
            ("foo", "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173734f7665726c6f6164732e666f6f3a31", "method", None,
             lambda: ([float], None)),
            ("bar", "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173734f7665726c6f6164732e626172", "method", None,
             lambda: ([str], None)),
            ("bar", "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d436c6173734f7665726c6f6164732e6261723a31", "method", None,
             lambda: ([float], None)),
            ("foo", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f", "method", None,
             lambda: ([], None)),
            ("foo", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e666f6f3a31", "method", None,
             lambda: ([int], None)),
            ("bar", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e626172", "method", None,
             lambda: ([], None)),
            ("baz", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e62617a", "method", None,
             lambda: ([], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ChildClassFromClassOverloads):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def foo(self, *args, **kwargs):
        return _wrap(generated.smoke_ChildClassFromClassOverloads.foo(self, *[_unwrap(a) for a in args], **{k: _unwrap(v) for k, v in kwargs.items()}), None)


    def bar(self, *args, **kwargs):
        return _wrap(generated.smoke_ChildClassFromClassOverloads.bar(self, *[_unwrap(a) for a in args], **{k: _unwrap(v) for k, v in kwargs.items()}), None)
