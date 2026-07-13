


class InternalInterfaceParent:
    """"""

    def __init__(self, native):
        self._native = native


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop


