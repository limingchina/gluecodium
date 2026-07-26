

import typing

from enum import Enum

import generated


class Season(Enum):
    """"""

    WINTER = generated.kotlin_smoke_Season.WINTER
    SPRING = generated.kotlin_smoke_Season.SPRING
    SUMMER = generated.kotlin_smoke_Season.SUMMER
    AUTUMN = generated.kotlin_smoke_Season.AUTUMN

    @property
    def _native(self):
        return self.value

