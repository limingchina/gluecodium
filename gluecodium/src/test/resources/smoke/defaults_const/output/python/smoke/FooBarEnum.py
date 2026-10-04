

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class FooBarEnum(Enum):

    FOO = generated.smoke_FooBarEnum.FOO
    BAR = generated.smoke_FooBarEnum.BAR
    BAZ = generated.smoke_FooBarEnum.BAZ

    @property
    def _native(self):
        return self.value
