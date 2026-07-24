

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    ALPHA = generated.Alphabet.ALPHA
    BETA = generated.Alphabet.BETA
    GAMMA = generated.Alphabet.GAMMA

    @property
    def _native(self):
        return self.value

