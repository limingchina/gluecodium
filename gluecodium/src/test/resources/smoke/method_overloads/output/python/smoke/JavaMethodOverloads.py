


class JavaMethodOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    def one(self, input: str):
        """"""
        return self._native.one(input)


    def two(self, input: list[str]):
        """"""
        return self._native.two(input)

