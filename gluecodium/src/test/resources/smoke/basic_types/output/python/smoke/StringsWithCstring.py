

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class StringsWithCstring(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def return_input_string_type(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return _wrap(generated.smoke_StringsWithCstring.return_input_string_type(_unwrap(input_string, str)), str)

    @staticmethod
    def return_input_string(input_string: str) -> str:
        """Method that takes a C string as input and returns an std::string it as output."""
        return _wrap(generated.smoke_StringsWithCstring.return_input_string(_unwrap(input_string, str)), str)
