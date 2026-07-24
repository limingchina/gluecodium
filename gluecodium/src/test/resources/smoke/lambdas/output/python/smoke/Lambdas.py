

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.LambdasConfuser import LambdasConfuser
from smoke.LambdasIndexer import LambdasIndexer
from smoke.LambdasProducer import LambdasProducer

from _native_base import _NativeBase

import generated


class Lambdas(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def deconfuse(self, value: str, confuser: LambdasConfuser) -> LambdasProducer:
        """"""
        return _wrap(self._native.deconfuse(_unwrap(value, str), _unwrap(confuser, LambdasConfuser)), LambdasProducer)

    @staticmethod
    def fuse(items: list[str], callback: LambdasIndexer) -> dict[int, str]:
        """"""
        return _wrap(generated.Lambdas.fuse(_unwrap(items, list[str]), _unwrap(callback, LambdasIndexer)), dict[int, str])

