

import typing

from enum import Enum

import generated


class SomeInternalEnum(Enum):
    """"""

    ONE = generated.SomeInternalEnum.ONE
    TWO = generated.SomeInternalEnum.TWO
    THREE = generated.SomeInternalEnum.THREE
    SINGLE = generated.SomeInternalEnum.SINGLE

    @property
    def _native(self):
        return self.value

