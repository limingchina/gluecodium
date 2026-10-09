

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.Payload import Payload

class WithPayloadError(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
