


class UseDartExternalGenerics:
    """"""

    def __init__(self, native):
        self._native = native


    def use_generics(self, list: list[Rectangle], set: set[CompressionState]) -> dict[CompressionState, Rectangle]:
        """"""
        return self._native.use_generics(list, set)

