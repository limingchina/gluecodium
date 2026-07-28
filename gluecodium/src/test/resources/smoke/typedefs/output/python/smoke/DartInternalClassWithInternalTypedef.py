

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class DartInternalClassWithInternalTypedef(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def numbers(self) -> dict[str, int]:
        """"""
        return _wrap(self._native.numbers, dict[str, int])

    @numbers.setter
    def numbers(self, value: dict[str, int]):
        self._native.numbers = _unwrap(value, dict[str, int])

    @property
    def labels(self) -> list[str]:
        """"""
        return _wrap(self._native.labels, list[str])

    @labels.setter
    def labels(self, value: list[str]):
        self._native.labels = _unwrap(value, list[str])

