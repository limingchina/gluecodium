

from __future__ import annotations



import generated


class AttributesInterface(generated.AttributesInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.AttributesInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def very_fun(self, param: str):
        """"""
        return generated.AttributesInterface.very_fun(self, param)

    @property
    def prop(self) -> str:
        """"""
        return generated.AttributesInterface.prop.fget(self)

    @prop.setter
    def prop(self, value: str):
        generated.AttributesInterface.prop.fset(self, value)


    PI = False

