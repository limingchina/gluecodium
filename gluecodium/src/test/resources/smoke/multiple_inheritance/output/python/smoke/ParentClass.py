


class ParentClass:
    """"""

    def __init__(self, native):
        self._native = native


    def parent_function(self):
        """"""
        return self._native.parent_function()


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property


