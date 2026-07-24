

import typing


import generated


class ParentNarrowOne(generated.ParentNarrowOne):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ParentNarrowOne):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def parent_function_one(self): ...

    @property
    def parent_property_one(self) -> str:
        """"""
        return _wrap(generated.ParentNarrowOne.parent_property_one.fget(self), str)

    @parent_property_one.setter
    def parent_property_one(self, value: str):
        generated.ParentNarrowOne.parent_property_one.fset(self, _unwrap(value, str))

