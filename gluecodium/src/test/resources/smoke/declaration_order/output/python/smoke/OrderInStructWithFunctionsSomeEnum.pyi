

import typing

from enum import Enum

import generated


class OrderInStructWithFunctionsSomeEnum(Enum):
    """"""

    FOO = generated.OrderInStructWithFunctionsSomeEnum.FOO
    BAR = generated.OrderInStructWithFunctionsSomeEnum.BAR

    @property
    def _native(self):
        return self.value

