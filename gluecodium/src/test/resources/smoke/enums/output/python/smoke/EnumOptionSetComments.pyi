

import typing

from enum import Enum

import generated


class EnumOptionSetComments(Enum):
    """"""

    ONE = generated.smoke_EnumOptionSetComments.ONE
    TWO = generated.smoke_EnumOptionSetComments.TWO
    THREE = generated.smoke_EnumOptionSetComments.THREE

    @property
    def _native(self):
        return self.value

