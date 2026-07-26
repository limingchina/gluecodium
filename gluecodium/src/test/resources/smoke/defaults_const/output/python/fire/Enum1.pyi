

import typing

from enum import Enum

import generated


class Enum1(Enum):
    """"""

    ENABLED = generated.fire_Enum1.ENABLED
    DISABLED = generated.fire_Enum1.DISABLED

    @property
    def _native(self):
        return self.value

