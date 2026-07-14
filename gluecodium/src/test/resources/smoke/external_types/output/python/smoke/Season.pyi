


from enum import Enum

import generated


class Season(Enum):
    """"""

    WINTER = generated.Season.WINTER
    SPRING = generated.Season.SPRING
    SUMMER = generated.Season.SUMMER
    AUTUMN = generated.Season.AUTUMN

    @property
    def _native(self):
        return self.value

