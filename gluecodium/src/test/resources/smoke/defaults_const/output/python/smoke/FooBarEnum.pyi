

import typing

from enum import Enum

import generated


class FooBarEnum(Enum):
    """"""

    FOO = generated.smoke_FooBarEnum.FOO
    BAR = generated.smoke_FooBarEnum.BAR
    BAZ = generated.smoke_FooBarEnum.BAZ

    @property
    def _native(self):
        return self.value

