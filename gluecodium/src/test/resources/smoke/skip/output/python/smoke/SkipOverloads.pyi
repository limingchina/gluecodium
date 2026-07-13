


from _native_base import _NativeBase


class SkipOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    dummy: float


    def do_foo(self, input: float):
        """"""
        return self._native.do_foo(input)

