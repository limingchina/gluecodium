

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class SkipProxy(generated.smoke_SkipProxy):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("not_in_java", "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4a617661", "method", None,
             lambda: ([str], str)),
            ("not_in_swift", "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e5377696674", "method", None,
             lambda: ([bool], bool)),
            ("not_in_dart", "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e44617274", "method", None,
             lambda: ([float], float)),
            ("not_in_kotlin", "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4b6f746c696e", "method", None,
             lambda: ([float], float)),
            ("skipped_in_java", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_get", "get", "get_skipped_in_java",
             lambda: ([], str)),
            ("skipped_in_java", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_set", "set", "set_skipped_in_java",
             lambda: ([str], None)),
            ("is_skipped_in_swift", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_get", "get", "is_skipped_in_swift",
             lambda: ([], bool)),
            ("is_skipped_in_swift", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_set", "set", "set_skipped_in_swift",
             lambda: ([bool], None)),
            ("skipped_in_dart", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_get", "get", "get_skipped_in_dart",
             lambda: ([], float)),
            ("skipped_in_dart", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_set", "set", "set_skipped_in_dart",
             lambda: ([float], None)),
            ("skipped_in_kotlin", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_get", "get", "get_skipped_in_kotlin",
             lambda: ([], float)),
            ("skipped_in_kotlin", "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_set", "set", "set_skipped_in_kotlin",
             lambda: ([float], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_SkipProxy):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def not_in_java(self, input: str) -> str:
        return _wrap(generated.smoke_SkipProxy.not_in_java(self, _unwrap(input, str)), str)

    def not_in_swift(self, input: bool) -> bool:
        return _wrap(generated.smoke_SkipProxy.not_in_swift(self, _unwrap(input, bool)), bool)

    def not_in_dart(self, input: float) -> float:
        return _wrap(generated.smoke_SkipProxy.not_in_dart(self, _unwrap(input, float)), float)

    def not_in_kotlin(self, input: float) -> float:
        return _wrap(generated.smoke_SkipProxy.not_in_kotlin(self, _unwrap(input, float)), float)

    @property
    def skipped_in_java(self) -> str:
        return _wrap(generated.smoke_SkipProxy.skipped_in_java.fget(self), str)

    @skipped_in_java.setter
    def skipped_in_java(self, value: str):
        generated.smoke_SkipProxy.skipped_in_java.fset(self, _unwrap(value, str))

    @property
    def is_skipped_in_swift(self) -> bool:
        return _wrap(generated.smoke_SkipProxy.is_skipped_in_swift.fget(self), bool)

    @is_skipped_in_swift.setter
    def is_skipped_in_swift(self, value: bool):
        generated.smoke_SkipProxy.is_skipped_in_swift.fset(self, _unwrap(value, bool))

    @property
    def skipped_in_dart(self) -> float:
        return _wrap(generated.smoke_SkipProxy.skipped_in_dart.fget(self), float)

    @skipped_in_dart.setter
    def skipped_in_dart(self, value: float):
        generated.smoke_SkipProxy.skipped_in_dart.fset(self, _unwrap(value, float))

    @property
    def skipped_in_kotlin(self) -> float:
        return _wrap(generated.smoke_SkipProxy.skipped_in_kotlin.fget(self), float)

    @skipped_in_kotlin.setter
    def skipped_in_kotlin(self, value: float):
        generated.smoke_SkipProxy.skipped_in_kotlin.fset(self, _unwrap(value, float))


