

import typing

from enum import Enum

import generated


class commentsSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.smoke_commentsSomeEnum.USELESS
    USEFUL = generated.smoke_commentsSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

