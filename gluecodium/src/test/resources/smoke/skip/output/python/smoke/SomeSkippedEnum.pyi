

import typing

from enum import Enum

import generated


class SomeSkippedEnum(Enum):
    """"""

    FOO = generated.smoke_SomeSkippedEnum.FOO

    @property
    def _native(self):
        return self.value

