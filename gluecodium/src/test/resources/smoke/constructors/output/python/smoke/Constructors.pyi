

from smoke.ConstructorsErrorEnum import ConstructorsErrorEnum
import typing

import generated


class Constructors(generated.Constructors):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.Constructors):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @typing.overload
    @staticmethod
    def create() -> Constructors: ...

    @typing.overload
    @staticmethod
    def create(other: Constructors) -> Constructors: ...

    @typing.overload
    @staticmethod
    def create(foo: str, bar: int) -> Constructors: ...

    @typing.overload
    @staticmethod
    def create(input: str) -> Constructors: ...

    @typing.overload
    @staticmethod
    def create(input: list[float]) -> Constructors: ...

    @typing.overload
    @staticmethod
    def create(input: int) -> Constructors: ...

