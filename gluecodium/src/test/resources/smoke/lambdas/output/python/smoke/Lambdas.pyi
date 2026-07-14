

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
        return generated.Lambdas.fuse(items, callback._native)

