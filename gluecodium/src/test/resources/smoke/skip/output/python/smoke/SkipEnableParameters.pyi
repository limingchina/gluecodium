


from _native_base import _NativeBase


class SkipEnableParameters(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_something(self, input: str):
        """"""
        return self._native.do_something(input)

