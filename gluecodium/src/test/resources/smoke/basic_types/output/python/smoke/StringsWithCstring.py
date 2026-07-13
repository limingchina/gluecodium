

from __future__ import annotations



from _native_base import _NativeBase

import generated


class StringsWithCstring(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    Method that takes a C string as input and returns an std::string it as output.
    def return_input_string_type(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        native_result = generated.StringsWithCstring.return_input_string_type(input_string)
        return str(native_result)

    @staticmethod
    Method that takes a C string as input and returns an std::string it as output.
    def return_input_string(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        native_result = generated.StringsWithCstring.return_input_string(input_string)
        return str(native_result)

