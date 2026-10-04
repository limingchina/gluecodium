

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


class Alphabet(Enum):

    ALPHA = generated.smoke_foo_Alphabet.ALPHA
    BETA = generated.smoke_foo_Alphabet.BETA
    GAMMA = generated.smoke_foo_Alphabet.GAMMA

    @property
    def _native(self):
        return self.value


