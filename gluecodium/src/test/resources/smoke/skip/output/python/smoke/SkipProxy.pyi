

from smoke.SkippedEverywhere import SkippedEverywhere
from smoke.SkippedEverywhereEnum import SkippedEverywhereEnum

from _native_base import _NativeBase


class SkipProxy(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


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



    @property
    def is_skipped_in_swift(self) -> bool:
        """"""
        return self._native.is_skipped_in_swift



    @property
    def skipped_in_dart(self) -> float:
        """"""
        return self._native.skipped_in_dart



    @property
    def skipped_in_kotlin(self) -> float:
        """"""
        return self._native.skipped_in_kotlin



    @property
    def skipped_everywhere(self) -> SkippedEverywhere:
        """"""
        return self._native.skipped_everywhere



    @property
    def skipped_everywhere_too(self) -> SkippedEverywhereEnum:
        """"""
        return self._native.skipped_everywhere_too


