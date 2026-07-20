

from smoke.SkippedEverywhere import SkippedEverywhere
from smoke.SkippedEverywhereEnum import SkippedEverywhereEnum
import typing


import generated


class SkipProxy(generated.SkipProxy):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.SkipProxy):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def not_in_java(self, input: str) -> str: ...

    def not_in_swift(self, input: bool) -> bool: ...

    def not_in_dart(self, input: float) -> float: ...

    def not_in_kotlin(self, input: float) -> float: ...

    @property
    def skipped_in_java(self) -> str:
        """"""
        return generated.SkipProxy.skipped_in_java.fget(self)

    @skipped_in_java.setter
    def skipped_in_java(self, value: str):
        generated.SkipProxy.skipped_in_java.fset(self, value)

    @property
    def is_skipped_in_swift(self) -> bool:
        """"""
        return generated.SkipProxy.is_skipped_in_swift.fget(self)

    @is_skipped_in_swift.setter
    def is_skipped_in_swift(self, value: bool):
        generated.SkipProxy.is_skipped_in_swift.fset(self, value)

    @property
    def skipped_in_dart(self) -> float:
        """"""
        return generated.SkipProxy.skipped_in_dart.fget(self)

    @skipped_in_dart.setter
    def skipped_in_dart(self, value: float):
        generated.SkipProxy.skipped_in_dart.fset(self, value)

    @property
    def skipped_in_kotlin(self) -> float:
        """"""
        return generated.SkipProxy.skipped_in_kotlin.fget(self)

    @skipped_in_kotlin.setter
    def skipped_in_kotlin(self, value: float):
        generated.SkipProxy.skipped_in_kotlin.fset(self, value)

    @property
    def skipped_everywhere(self) -> SkippedEverywhere:
        """"""
        return generated.SkipProxy.skipped_everywhere.fget(self)

    @skipped_everywhere.setter
    def skipped_everywhere(self, value: SkippedEverywhere):
        generated.SkipProxy.skipped_everywhere.fset(self, value)

    @property
    def skipped_everywhere_too(self) -> SkippedEverywhereEnum:
        """"""
        return generated.SkipProxy.skipped_everywhere_too.fget(self)

    @skipped_everywhere_too.setter
    def skipped_everywhere_too(self, value: SkippedEverywhereEnum):
        generated.SkipProxy.skipped_everywhere_too.fset(self, value)

