

from smoke.ConstructorsErrorEnum import ConstructorsErrorEnum

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

    @staticmethod
    def create() -> Constructors:
        """"""
        native_result = generated.Constructors.create()
        return Constructors(native_result)

    @staticmethod
    def create(other: Constructors) -> Constructors:
        """"""
        native_result = generated.Constructors.create(other._native)
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

