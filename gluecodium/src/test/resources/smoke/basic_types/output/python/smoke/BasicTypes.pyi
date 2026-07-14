



from _native_base import _NativeBase

import generated


class BasicTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def string_function(input: str) -> str:
        """"""
        return generated.BasicTypes.string_function(input)

    @staticmethod
    def bool_function(input: bool) -> bool:
        """"""
        return generated.BasicTypes.bool_function(input)

    @staticmethod
    def float_function(input: float) -> float:
        """"""
        return generated.BasicTypes.float_function(input)

    @staticmethod
    def double_function(input: float) -> float:
        """"""
        return generated.BasicTypes.double_function(input)

    @staticmethod
    def byte_function(input: int) -> int:
        """"""
        return generated.BasicTypes.byte_function(input)

    @staticmethod
    def short_function(input: int) -> int:
        """"""
        return generated.BasicTypes.short_function(input)

    @staticmethod
    def int_function(input: int) -> int:
        """"""
        return generated.BasicTypes.int_function(input)

    @staticmethod
    def long_function(input: int) -> int:
        """"""
        return generated.BasicTypes.long_function(input)

    @staticmethod
    def ubyte_function(input: int) -> int:
        """"""
        return generated.BasicTypes.ubyte_function(input)

    @staticmethod
    def ushort_function(input: int) -> int:
        """"""
        return generated.BasicTypes.ushort_function(input)

    @staticmethod
    def uint_function(input: int) -> int:
        """"""
        return generated.BasicTypes.uint_function(input)

    @staticmethod
    def ulong_function(input: int) -> int:
        """"""
        return generated.BasicTypes.ulong_function(input)

