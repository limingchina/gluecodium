


class SkipOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    dummy: float


    def do_foo(self, input: float):
        """"""
        return self._native.do_foo(input)

