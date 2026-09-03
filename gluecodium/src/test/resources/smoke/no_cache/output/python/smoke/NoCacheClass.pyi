

from enum import Enum
import typing

class NoCacheClass:

    @staticmethod
    def make() -> NoCacheClass:
        ...

    def foo(self):
        ...


