

from smoke.LambdasConfuser import LambdasConfuser
from smoke.LambdasIndexer import LambdasIndexer
from smoke.LambdasProducer import LambdasProducer
import typing
from typing import Callable

class Lambdas:

    def deconfuse(self, value: str, confuser: Callable[[str], Callable[[], str]]) -> Callable[[], str]:
        ...

    @staticmethod
    def fuse(items: list[str], callback: Callable[[str, float], int]) -> dict[int, str]:
        ...

