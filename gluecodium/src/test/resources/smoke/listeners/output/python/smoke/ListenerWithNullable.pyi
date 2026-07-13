


from _native_base import _NativeBase


class ListenerWithNullable(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_byte(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_byte(input)


    def method_with_u_byte(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_u_byte(input)


    def method_with_short(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_short(input)


    def method_with_u_short(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_u_short(input)


    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_int(input)


    def method_with_u_int(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_u_int(input)


    def method_with_long(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_long(input)


    def method_with_u_long(self, input: Optional[int]) -> Optional[int]:
        """"""
        return self._native.method_with_u_long(input)


    def method_with_double(self, input: Optional[bool]) -> Optional[bool]:
        """"""
        return self._native.method_with_double(input)


    def method_with_float(self, input: Optional[float]) -> Optional[float]:
        """"""
        return self._native.method_with_float(input)


    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        """"""
        return self._native.method_with_double(input)

