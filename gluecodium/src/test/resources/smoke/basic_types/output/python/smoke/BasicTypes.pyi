



from _native_base import _NativeBase

import generated


class BasicTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def string_function(input: str) -> str:
        """"""
        native_result = generated.BasicTypes.string_function(input)
        return str(native_result)

    @staticmethod

    def bool_function(input: bool) -> bool:
        """"""
        native_result = generated.BasicTypes.bool_function(input)
        return bool(native_result)

    @staticmethod

    def float_function(input: float) -> float:
        """"""
        native_result = generated.BasicTypes.float_function(input)
        return float(native_result)

    @staticmethod

    def double_function(input: float) -> float:
        """"""
        native_result = generated.BasicTypes.double_function(input)
        return float(native_result)

    @staticmethod

    def byte_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.byte_function(input)
        return int(native_result)

    @staticmethod

    def short_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.short_function(input)
        return int(native_result)

    @staticmethod

    def int_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.int_function(input)
        return int(native_result)

    @staticmethod

    def long_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.long_function(input)
        return int(native_result)

    @staticmethod

    def ubyte_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.ubyte_function(input)
        return int(native_result)

    @staticmethod

    def ushort_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.ushort_function(input)
        return int(native_result)

    @staticmethod

    def uint_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.uint_function(input)
        return int(native_result)

    @staticmethod

    def ulong_function(input: int) -> int:
        """"""
        native_result = generated.BasicTypes.ulong_function(input)
        return int(native_result)

