

import typing

from enum import Enum

import generated


class Enum1(Enum):
    """"""

    ENABLED = generated.Enum1.ENABLED
    DISABLED = generated.Enum1.DISABLED

    @property
    def _native(self):
        return self.value

