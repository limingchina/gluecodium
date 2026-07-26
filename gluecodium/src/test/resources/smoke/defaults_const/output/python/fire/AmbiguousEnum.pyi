

import typing

from enum import Enum

import generated


class AmbiguousEnum(Enum):
    """"""

    DISABLED = generated.fire_AmbiguousEnum.DISABLED

    @property
    def _native(self):
        return self.value

