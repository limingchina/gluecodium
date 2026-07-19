



import generated


class ListenerWithNullable(generated.ListenerWithNullable):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ListenerWithNullable):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def method_with_byte(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_byte(self, input)

    def method_with_u_byte(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_u_byte(self, input)

    def method_with_short(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_short(self, input)

    def method_with_u_short(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_u_short(self, input)

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_int(self, input)

    def method_with_u_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_u_int(self, input)

    def method_with_long(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_long(self, input)

    def method_with_u_long(self, input: Optional[int]) -> Optional[int]:
        """"""
        return generated.ListenerWithNullable.method_with_u_long(self, input)

    def method_with_double(self, input: Optional[bool]) -> Optional[bool]:
        """"""
        return generated.ListenerWithNullable.method_with_double(self, input)

    def method_with_float(self, input: Optional[float]) -> Optional[float]:
        """"""
        return generated.ListenerWithNullable.method_with_float(self, input)

    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        """"""
        return generated.ListenerWithNullable.method_with_double(self, input)

