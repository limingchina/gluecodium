



import generated


class InterfaceWithStatic(generated.InterfaceWithStatic):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.InterfaceWithStatic):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def regular_function(self) -> str:
        """"""
        return generated.InterfaceWithStatic.regular_function(self)

    @staticmethod
    def static_function() -> str:
        """"""
        return generated.InterfaceWithStatic.static_function()

    @property
    def regular_property(self) -> str:
        """"""
        return generated.InterfaceWithStatic.regular_property.fget(self)

    @regular_property.setter
    def regular_property(self, value: str):
        generated.InterfaceWithStatic.regular_property.fset(self, value)


    @staticmethod
    def static_property() -> str:
        """"""
        return generated.InterfaceWithStatic.static_property()

