

import typing

from enum import Enum

import generated


class FooBarEnum(Enum):
    """"""

    FOO = generated.FooBarEnum.FOO
    BAR = generated.FooBarEnum.BAR
    BAZ = generated.FooBarEnum.BAZ

    @property
    def _native(self):
        return self.value

