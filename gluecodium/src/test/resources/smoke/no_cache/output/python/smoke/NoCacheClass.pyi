

from enum import Enum
import typing
from typing import Optional

class NoCacheClass:

    @staticmethod
    def make() -> NoCacheClass:
        ...

    def foo(self):
        ...
