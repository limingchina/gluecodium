

from smoke.ChildConstructors import ChildConstructors
from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.Constructors import Constructors
from smoke.ErrorEnum import ErrorEnum

class ChildConstructors(
    Constructors):
    """"""

    def __init__(self, native):
        self._native = native


    def create(self) -> ChildConstructors:
        """"""
        return self._native.create()


    def create(self, other: Constructors) -> ChildConstructors:
        """"""
        return self._native.create(other)

