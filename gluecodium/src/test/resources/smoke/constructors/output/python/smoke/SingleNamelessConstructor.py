

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SingleNamelessConstructor(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> SingleNamelessConstructor:
        native_result = generated.smoke_SingleNamelessConstructor.create()
        return _get_or_create_wrapper(native_result, SingleNamelessConstructor)


