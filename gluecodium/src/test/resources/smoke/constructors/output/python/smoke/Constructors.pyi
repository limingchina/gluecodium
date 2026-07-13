

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.ErrorEnum import ErrorEnum


from _native_base import _NativeBase

import generated


class Constructors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def create() -> Constructors:
        """"""
        native_result = generated.Constructors.create()
        return Constructors(native_result)

    @staticmethod

    def create(other: Constructors) -> Constructors:
        """"""
        native_result = generated.Constructors.create(other)
        return Constructors(native_result)

    @staticmethod

    def create(foo: str, bar: int) -> Constructors:
        """"""
        native_result = generated.Constructors.create(foo, bar)
        return Constructors(native_result)

    @staticmethod

    def create(input: str) -> Constructors:
        """"""
        native_result = generated.Constructors.create(input)
        return Constructors(native_result)

    @staticmethod

    def create(input: list[float]) -> Constructors:
        """"""
        native_result = generated.Constructors.create(input)
        return Constructors(native_result)

    @staticmethod

    def create(input: int) -> Constructors:
        """"""
        native_result = generated.Constructors.create(input)
        return Constructors(native_result)

