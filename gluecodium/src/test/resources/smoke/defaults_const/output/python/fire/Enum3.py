

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


class Enum3(Enum):

    ENABLED = generated.fire_Enum3.ENABLED
    DISABLED = generated.fire_Enum3.DISABLED

    @property
    def _native(self):
        return self.value


