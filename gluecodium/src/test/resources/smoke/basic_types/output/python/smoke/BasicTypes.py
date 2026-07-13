


class BasicTypes:
    """"""

    def __init__(self, native):
        self._native = native


    def string_function(self, input: str) -> str:
        """"""
        return self._native.string_function(input)


    def bool_function(self, input: bool) -> bool:
        """"""
        return self._native.bool_function(input)


    def float_function(self, input: float) -> float:
        """"""
        return self._native.float_function(input)


    def double_function(self, input: float) -> float:
        """"""
        return self._native.double_function(input)


    def byte_function(self, input: int) -> int:
        """"""
        return self._native.byte_function(input)


    def short_function(self, input: int) -> int:
        """"""
        return self._native.short_function(input)


    def int_function(self, input: int) -> int:
        """"""
        return self._native.int_function(input)


    def long_function(self, input: int) -> int:
        """"""
        return self._native.long_function(input)


    def ubyte_function(self, input: int) -> int:
        """"""
        return self._native.ubyte_function(input)


    def ushort_function(self, input: int) -> int:
        """"""
        return self._native.ushort_function(input)


    def uint_function(self, input: int) -> int:
        """"""
        return self._native.uint_function(input)


    def ulong_function(self, input: int) -> int:
        """"""
        return self._native.ulong_function(input)

