

from __future__ import annotations


from enum import Enum

import generated


class SerializationSomeEnum(Enum):
    """"""

    FOO = generated.SerializationSomeEnum.FOO
    BAR = generated.SerializationSomeEnum.BAR

    @property
    def _native(self):
        return self.value

