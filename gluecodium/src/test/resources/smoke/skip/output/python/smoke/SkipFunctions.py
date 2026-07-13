


class SkipFunctions:
    """"""

    def __init__(self, native):
        self._native = native


    def not_in_java(self, input: str) -> str:
        """"""
        return self._native.not_in_java(input)


    def not_in_swift(self, input: bool) -> bool:
        """"""
        return self._native.not_in_swift(input)


    def not_in_dart(self, input: float) -> float:
        """"""
        return self._native.not_in_dart(input)


    def not_in_kotlin(self, input: str) -> str:
        """"""
        return self._native.not_in_kotlin(input)

