

import typing

from enum import Enum

import generated


class StructsFooBar(Enum):
    """"""

    FOO = generated.StructsFooBar.FOO
    BAR = generated.StructsFooBar.BAR

    @property
    def _native(self):
        return self.value

