


class OuterInternalInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def some_function(self) -> int:
        """"""
        return self._native.some_function()

