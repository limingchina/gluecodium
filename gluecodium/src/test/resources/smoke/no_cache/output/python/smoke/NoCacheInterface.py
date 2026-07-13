


class NoCacheInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def foo(self):
        """"""
        return self._native.foo()

