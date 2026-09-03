

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class AttributesCrashError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


