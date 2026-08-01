

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
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


