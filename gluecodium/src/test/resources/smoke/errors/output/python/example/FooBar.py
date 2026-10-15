

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.Errors import Errors
from smoke.SomeTypeCollection import SomeTypeCollection

class FooBar(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_internal_error():
        generated.example_FooBar.method_with_internal_error()

    @staticmethod
    def method_with_type_collection_error():
        generated.example_FooBar.method_with_type_collection_error()
