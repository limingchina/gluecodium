

import typing

from enum import Enum

import generated


class SerializationSomeEnum(Enum):
    """"""

    FOO = generated.smoke_SerializationSomeEnum.FOO
    BAR = generated.smoke_SerializationSomeEnum.BAR

    @property
    def _native(self):
        return self.value

