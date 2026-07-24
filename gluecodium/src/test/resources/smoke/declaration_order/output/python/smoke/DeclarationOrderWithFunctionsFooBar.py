

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct

class DeclarationOrderWithFunctionsFooBar(Exception):
    """"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

