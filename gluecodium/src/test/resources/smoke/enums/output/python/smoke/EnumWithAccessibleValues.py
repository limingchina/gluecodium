

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class EnumWithAccessibleValues(Enum):

    FOO = generated.smoke_EnumWithAccessibleValues.FOO
    BAR = generated.smoke_EnumWithAccessibleValues.BAR
    BAZ = generated.smoke_EnumWithAccessibleValues.BAZ
    FOO_ALIAS = generated.smoke_EnumWithAccessibleValues.FOO_ALIAS

    @property
    def _native(self):
        return self.value
