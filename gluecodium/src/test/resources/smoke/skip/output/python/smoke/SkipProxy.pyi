

from smoke.SkippedEverywhere import SkippedEverywhere
from smoke.SkippedEverywhereEnum import SkippedEverywhereEnum


from _native_base import _NativeBase

import generated


class SkipProxy(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, SkipProxy):
            super().__init__(native)
        else:
            super().__init__(generated.SkipProxy())


    def not_in_java(self, input: str) -> str:
        """"""
        return self._native.not_in_java(input)


    def not_in_swift(self, input: bool) -> bool:
        """"""
        return self._native.not_in_swift(input)


    def not_in_dart(self, input: float) -> float:
        """"""
        return self._native.not_in_dart(input)


    def not_in_kotlin(self, input: float) -> float:
        """"""
        return self._native.not_in_kotlin(input)


    @property
    def skipped_in_java(self) -> str:
        """"""
        return self._native.skipped_in_java

    @skipped_in_java.setter
    def skipped_in_java(self, value: str):
        self._native.skipped_in_java = value


    @property
    def is_skipped_in_swift(self) -> bool:
        """"""
        return self._native.is_skipped_in_swift

    @is_skipped_in_swift.setter
    def is_skipped_in_swift(self, value: bool):
        self._native.is_skipped_in_swift = value


    @property
    def skipped_in_dart(self) -> float:
        """"""
        return self._native.skipped_in_dart

    @skipped_in_dart.setter
    def skipped_in_dart(self, value: float):
        self._native.skipped_in_dart = value


    @property
    def skipped_in_kotlin(self) -> float:
        """"""
        return self._native.skipped_in_kotlin

    @skipped_in_kotlin.setter
    def skipped_in_kotlin(self, value: float):
        self._native.skipped_in_kotlin = value


    @property
    def skipped_everywhere(self) -> SkippedEverywhere:
        """"""
        return self._native.skipped_everywhere

    @skipped_everywhere.setter
    def skipped_everywhere(self, value: SkippedEverywhere):
        self._native.skipped_everywhere = value


    @property
    def skipped_everywhere_too(self) -> SkippedEverywhereEnum:
        """"""
        return self._native.skipped_everywhere_too

    @skipped_everywhere_too.setter
    def skipped_everywhere_too(self, value: SkippedEverywhereEnum):
        self._native.skipped_everywhere_too = value

