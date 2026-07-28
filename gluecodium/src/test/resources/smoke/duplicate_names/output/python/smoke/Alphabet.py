

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    A = generated.smoke_Alphabet.A
    B = generated.smoke_Alphabet.B
    C = generated.smoke_Alphabet.C

    @property
    def _native(self):
        return self.value

