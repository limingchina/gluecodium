

import typing

from enum import Enum

import generated


class Enum4(Enum):
    """"""

    ENABLED = generated.Enum4.ENABLED
    DISABLED = generated.Enum4.DISABLED

    @property
    def _native(self):
        return self.value

