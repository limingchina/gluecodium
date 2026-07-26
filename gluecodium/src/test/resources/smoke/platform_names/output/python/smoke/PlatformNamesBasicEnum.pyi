

import typing

from enum import Enum

import generated


class PlatformNamesBasicEnum(Enum):
    """"""

    BASIC_ITEM = generated.smoke_PlatformNamesBasicEnum.foo_item

    @property
    def _native(self):
        return self.value

