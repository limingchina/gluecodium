

import typing


import generated


class SkipSetter(generated.smoke_SkipSetter):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_SkipSetter):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def foo(self) -> str:
        """"""
        return _wrap(generated.smoke_SkipSetter.foo.fget(self), str)

    @foo.setter
    def foo(self, value: str):
        generated.smoke_SkipSetter.foo.fset(self, _unwrap(value, str))

