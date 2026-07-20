

from __future__ import annotations


from _native_base import _NativeBase

import generated


class StringsWithCstring(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def return_input_string_type(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return generated.StringsWithCstring.return_input_string_type(input_string)

    @staticmethod
    def return_input_string(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return generated.StringsWithCstring.return_input_string(input_string)

