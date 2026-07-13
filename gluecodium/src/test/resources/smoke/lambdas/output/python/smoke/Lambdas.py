

from __future__ import annotations

from smoke.Confuser import Confuser
from smoke.Indexer import Indexer
from smoke.Producer import Producer


from _native_base import _NativeBase

import generated


class Lambdas(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def deconfuse(self, value: str, confuser: Confuser) -> Producer:
        """"""
        return self._native.deconfuse(value, confuser._native)

    @staticmethod

    def fuse(items: list[str], callback: Indexer) -> dict[int, str]:
        """"""
        native_result = generated.Lambdas.fuse(items, callback)
        return dict[int, str](native_result)

