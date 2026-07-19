

from __future__ import annotations

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
        return self._native.deconfuse(value, confuser._native)

    @staticmethod
    def fuse(items: list[str], callback: LambdasIndexer) -> dict[int, str]:
        """"""
        return generated.Lambdas.fuse(items, callback._native)

