

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SkipProxy(generated.smoke_SkipProxy):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_SkipProxy):
            super().__init__(native)
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


