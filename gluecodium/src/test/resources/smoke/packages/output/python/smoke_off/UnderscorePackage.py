

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class UnderscorePackage(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def basic_method(input_string: str) -> str:
        """"""
        return generated.UnderscorePackage.basic_method(_unwrap(input_string, str))

