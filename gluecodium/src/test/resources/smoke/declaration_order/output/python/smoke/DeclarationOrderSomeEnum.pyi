

import typing

from enum import Enum

import generated


class DeclarationOrderSomeEnum(Enum):
    """"""

    FOO = generated.smoke_DeclarationOrderSomeEnum.FOO
    BAR = generated.smoke_DeclarationOrderSomeEnum.BAR

    @property
    def _native(self):
        return self.value

