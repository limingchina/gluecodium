

from __future__ import annotations


from enum import Enum

import generated


class DontSmokeEnum(Enum):
    """"""

    FOO = generated.DontSmokeEnum.FOO

    @property
    def _native(self):
        return self.value

