

import typing

from enum import Enum

import generated


class StructsFooBar(Enum):
    """"""

    FOO = generated.smoke_StructsFooBar.FOO
    BAR = generated.smoke_StructsFooBar.BAR

    @property
    def _native(self):
        return self.value

