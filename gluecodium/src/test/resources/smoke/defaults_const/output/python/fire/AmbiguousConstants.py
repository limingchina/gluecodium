

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.SomeStruct import SomeStruct

from _native_base import _NativeBase

import generated


class AmbiguousConstants(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    DUMMY = {42}

