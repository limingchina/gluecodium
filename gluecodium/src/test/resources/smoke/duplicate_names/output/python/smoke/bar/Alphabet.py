

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    ALEPH = generated.smoke_bar_Alphabet.ALEPH
    BEIT = generated.smoke_bar_Alphabet.BEIT
    GIMEL = generated.smoke_bar_Alphabet.GIMEL

    @property
    def _native(self):
        return self.value

