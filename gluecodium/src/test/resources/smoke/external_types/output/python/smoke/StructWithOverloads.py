


class StructWithOverloads:
    """"""

    def __init__(self, native):
        self._native = native


    overloaded_accessors: int


    def overloaded_method(self) -> str:
        """"""
        return self._native.overloaded_method()


    def overloaded_method(self, input: str) -> str:
        """"""
        return self._native.overloaded_method(input)


    def overloaded_method(self, input_string: str, input_bool: bool) -> str:
        """"""
        return self._native.overloaded_method(input_string, input_bool)

