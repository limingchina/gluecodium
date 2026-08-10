

from enum import Enum
import typing

class ListenerWithNullable:

    def method_with_byte(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_u_byte(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_short(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_u_short(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_int(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_u_int(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_long(self, input: Optional[int]) -> Optional[int]:
        ...

    def method_with_u_long(self, input: Optional[int]) -> Optional[int]:
        ...

    @typing.overload
    def method_with_double(self, input: Optional[bool]) -> Optional[bool]:
        ...

    def method_with_float(self, input: Optional[float]) -> Optional[float]:
        ...

    @typing.overload
    def method_with_double(self, input: Optional[float]) -> Optional[float]:
        ...


