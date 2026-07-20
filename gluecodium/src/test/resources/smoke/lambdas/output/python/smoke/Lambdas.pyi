

from smoke.LambdasConfuser import LambdasConfuser
from smoke.LambdasIndexer import LambdasIndexer
from smoke.LambdasProducer import LambdasProducer
import typing

from _native_base import _NativeBase

import generated


class Lambdas(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def deconfuse(self, value: str, confuser: LambdasConfuser) -> LambdasProducer: ...

    @staticmethod
    def fuse(items: list[str], callback: LambdasIndexer) -> dict[int, str]: ...

