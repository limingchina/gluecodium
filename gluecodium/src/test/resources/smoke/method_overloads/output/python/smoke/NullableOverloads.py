


class NullableOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def foo(self, input: Optional[str]):
        """"""
        return self._native.foo(input)

