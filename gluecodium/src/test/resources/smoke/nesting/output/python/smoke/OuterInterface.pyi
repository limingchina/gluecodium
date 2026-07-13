


from _native_base import _NativeBase


class OuterInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, input: str) -> str:
        """"""
        return self._native.foo(input)

