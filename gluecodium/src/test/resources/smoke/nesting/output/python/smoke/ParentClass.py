


class ParentClass:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_fun(self):
        """"""
        return self._native.parent_fun()


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property


