

import typing

from enum import Enum

import generated


class NullableSomeEnum(Enum):
    """"""

    ON = generated.smoke_NullableSomeEnum.ON
    OFF = generated.smoke_NullableSomeEnum.OFF

    @property
    def _native(self):
        return self.value

