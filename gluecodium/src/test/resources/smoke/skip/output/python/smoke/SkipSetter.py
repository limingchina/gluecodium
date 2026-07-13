


class SkipSetter:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def foo(self) -> str:
        """"""
        return self._native.foo


