

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.Constructors import Constructors
from smoke.ErrorEnum import ErrorEnum

class Constructors:
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> Constructors:
        """"""
        return self._native.create()


    def create(self, other: Constructors) -> Constructors:
        """"""
        return self._native.create(other)


    def create(self, foo: str, bar: int) -> Constructors:
        """"""
        return self._native.create(foo, bar)


    def create(self, input: str) -> Constructors:
        """"""
        return self._native.create(input)


    def create(self, input: list[float]) -> Constructors:
        """"""
        return self._native.create(input)


    def create(self, input: int) -> Constructors:
        """"""
        return self._native.create(input)

