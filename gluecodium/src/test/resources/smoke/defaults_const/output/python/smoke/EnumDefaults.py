

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
from smoke.EnumWrapper import EnumWrapper

from _native_base import _NativeBase

import generated


class EnumDefaults(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

