


from _native_base import _NativeBase


class OuterClassWithLambdaAndProperty(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def some_integer(self) -> int:
        """"""
        return self._native.some_integer



    @property
    def another_integer(self) -> int:
        """"""
        return self._native.another_integer


