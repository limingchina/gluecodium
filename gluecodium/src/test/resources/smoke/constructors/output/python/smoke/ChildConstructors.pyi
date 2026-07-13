

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.Constructors import Constructors
from smoke.ErrorEnum import ErrorEnum


from _native_base import _NativeBase

import generated


class ChildConstructors(
    Constructors)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def create() -> ChildConstructors:
        """"""
        native_result = generated.ChildConstructors.create()
        return ChildConstructors(native_result)

    @staticmethod

    def create(other: Constructors) -> ChildConstructors:
        """"""
        native_result = generated.ChildConstructors.create(other)
        return ChildConstructors(native_result)

