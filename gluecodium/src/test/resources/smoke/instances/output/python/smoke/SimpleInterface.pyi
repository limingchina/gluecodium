



import generated


class SimpleInterface(generated.SimpleInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.SimpleInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def get_string_value(self) -> str:
        """"""
        return generated.SimpleInterface.get_string_value(self)

    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        """"""
        return generated.SimpleInterface.use_simple_interface(self, input._native)

