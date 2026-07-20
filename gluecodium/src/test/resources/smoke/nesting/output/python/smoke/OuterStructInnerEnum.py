

from __future__ import annotations


from enum import Enum

import generated


class OuterStructInnerEnum(Enum):
    """"""

    FOO = generated.OuterStructInnerEnum.FOO
    BAR = generated.OuterStructInnerEnum.BAR

    @property
    def _native(self):
        return self.value

