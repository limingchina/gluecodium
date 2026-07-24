

import typing


import generated


class DeprecationCommentsOnly(generated.DeprecationCommentsOnly):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.DeprecationCommentsOnly):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def some_method_with_all_comments(self, input: str) -> bool: ...

    @property
    def is_some_property(self) -> bool:
        """"""
        return _wrap(generated.DeprecationCommentsOnly.is_some_property.fget(self), bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        generated.DeprecationCommentsOnly.is_some_property.fset(self, _unwrap(value, bool))


    VERY_USEFUL = True

