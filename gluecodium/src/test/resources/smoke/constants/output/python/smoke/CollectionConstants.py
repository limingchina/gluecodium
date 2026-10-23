

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class CollectionConstants(_NativeBase):
    def __init__(self, native):
        super().__init__(native)


    LIST_CONSTANT = ["foo", "bar"]

    SET_CONSTANT = {"foo", "bar"}

    MAP_CONSTANT = {"foo": "bar"}

    MIXED_CONSTANT = {tuple(["foo"]): {"bar"}}
