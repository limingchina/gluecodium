

from __future__ import annotations


from enum import Enum

import generated


class NullableSomeEnum(Enum):
    """"""

    ON = generated.NullableSomeEnum.ON
    OFF = generated.NullableSomeEnum.OFF

    @property
    def _native(self):
        return self.value

