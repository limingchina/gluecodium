

from __future__ import annotations


from enum import Enum

import generated


class DeclarationOrderSomeEnum(Enum):
    """"""

    FOO = generated.DeclarationOrderSomeEnum.FOO
    BAR = generated.DeclarationOrderSomeEnum.BAR

    @property
    def _native(self):
        return self.value

