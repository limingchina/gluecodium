


class InternalClassWithStaticProperty:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def foo_bar(self) -> str:
        """"""
        return self._native.foo_bar


