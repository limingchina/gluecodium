


class OuterClassWithLambdaAndProperty:
    """"""

    def __init__(self, native):
        self._native = native


    @property
    def some_integer(self) -> int:
        """"""
        return self._native.some_integer



    @property
    def another_integer(self) -> int:
        """"""
        return self._native.another_integer


