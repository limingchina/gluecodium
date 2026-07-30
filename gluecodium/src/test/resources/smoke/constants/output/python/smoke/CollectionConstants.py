

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class CollectionConstants(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    LIST_CONSTANT = ["foo", "bar"]

    SET_CONSTANT = ["foo", "bar"]

    MAP_CONSTANT = ["foo": "bar"]

    MIXED_CONSTANT = [["foo"]: ["bar"]]

