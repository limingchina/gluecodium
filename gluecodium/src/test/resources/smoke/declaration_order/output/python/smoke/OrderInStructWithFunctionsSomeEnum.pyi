

import typing

from enum import Enum

import generated


class OrderInStructWithFunctionsSomeEnum(Enum):
    """"""

    FOO = generated.smoke_OrderInStructWithFunctionsSomeEnum.FOO
    BAR = generated.smoke_OrderInStructWithFunctionsSomeEnum.BAR

    @property
    def _native(self):
        return self.value

