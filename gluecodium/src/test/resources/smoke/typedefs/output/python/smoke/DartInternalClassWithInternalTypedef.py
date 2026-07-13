

from __future__ import annotations

from smoke.dict[str, int] import dict[str, int]
from smoke.list[str] import list[str]


from _native_base import _NativeBase

import generated


class DartInternalClassWithInternalTypedef(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def numbers(self) -> dict[str, int]:
        """"""
        return self._native.numbers

    @numbers.setter
    def numbers(self, value: dict[str, int]):
        self._native.numbers = value


    @property
    def labels(self) -> list[str]:
        """"""
        return self._native.labels

    @labels.setter
    def labels(self, value: list[str]):
        self._native.labels = value

