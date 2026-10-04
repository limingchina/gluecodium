

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


class Season(Enum):

    WINTER = generated.kotlin_smoke_Season.WINTER
    SPRING = generated.kotlin_smoke_Season.SPRING
    SUMMER = generated.kotlin_smoke_Season.SUMMER
    AUTUMN = generated.kotlin_smoke_Season.AUTUMN

    @property
    def _native(self):
        return self.value


