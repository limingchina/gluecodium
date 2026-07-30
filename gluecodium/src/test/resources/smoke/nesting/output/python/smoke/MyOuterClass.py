

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.MyParentInterface import MyParentInterface

from _native_base import _NativeBase

import generated


class MyOuterClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

