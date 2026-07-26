

from smoke.SpecialNamesInterfaceCallback import SpecialNamesInterfaceCallback
import typing
from typing import Callable


import generated


class SpecialNamesInterface(generated.smoke_SpecialNamesInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_SpecialNamesInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def dispatch(self, callback: Callable[[], None]): ...

