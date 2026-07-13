

from smoke.ChildConstructors import ChildConstructors
from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.Constructors import Constructors
from smoke.ErrorEnum import ErrorEnum

from _native_base import _NativeBase


class ChildConstructors(
    Constructors)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self) -> ChildConstructors:
        """"""
        return self._native.create()


    def create(self, other: Constructors) -> ChildConstructors:
        """"""
        return self._native.create(other)

