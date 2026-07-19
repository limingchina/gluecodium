

from __future__ import annotations

from smoke.ParentClass import ParentClass

import generated


class ForwardDeclarationBug(generated.ForwardDeclarationBug):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.ForwardDeclarationBug):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def foo(self, bar: ParentClass):
        """"""
        return generated.ForwardDeclarationBug.foo(self, bar._native)

