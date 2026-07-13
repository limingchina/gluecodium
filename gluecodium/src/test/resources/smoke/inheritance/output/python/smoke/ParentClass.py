


class ParentClass:
    """"""

    def __init__(self, native):
        self._native = native


    def root_method(self):
        """"""
        return self._native.root_method()


    @property
    def root_property(self) -> str:
        """"""
        return self._native.root_property


