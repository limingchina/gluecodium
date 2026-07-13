

from smoke.Confuser import Confuser
from smoke.Indexer import Indexer
from smoke.Producer import Producer

class Lambdas:
    """"""

    def __init__(self, native):
        self._native = native


    def deconfuse(self, value: str, confuser: Confuser) -> Producer:
        """"""
        return self._native.deconfuse(value, confuser)


    def fuse(self, items: list[str], callback: Indexer) -> dict[int, str]:
        """"""
        return self._native.fuse(items, callback)

