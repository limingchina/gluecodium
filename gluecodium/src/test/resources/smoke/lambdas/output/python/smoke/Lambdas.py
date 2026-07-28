

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional
from typing import Callable

from smoke.LambdasConfuser import LambdasConfuser
from smoke.LambdasIndexer import LambdasIndexer
from smoke.LambdasProducer import LambdasProducer

from _native_base import _NativeBase

import generated


class Lambdas(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def deconfuse(self, value: str, confuser: Callable[[str], Callable[[], str]]) -> Callable[[], str]:
        """"""
        return _wrap(self._native.deconfuse(_unwrap(value, str), _unwrap(confuser, Callable[[str], Callable[[], str]])), Callable[[], str])

    @staticmethod
    def fuse(items: list[str], callback: Callable[[str, float], int]) -> dict[int, str]:
        """"""
        return _wrap(generated.smoke_Lambdas.fuse(_unwrap(items, list[str]), _unwrap(callback, Callable[[str, float], int])), dict[int, str])

