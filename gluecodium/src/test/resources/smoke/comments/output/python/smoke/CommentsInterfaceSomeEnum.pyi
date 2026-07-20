

import typing

from enum import Enum

import generated


class CommentsInterfaceSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.CommentsInterfaceSomeEnum.USELESS
    USEFUL = generated.CommentsInterfaceSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

