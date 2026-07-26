

import typing

from enum import Enum

import generated


class AttributesEnum(Enum):
    """"""

    NOPE = generated.smoke_AttributesEnum.NOPE

    @property
    def _native(self):
        return self.value

