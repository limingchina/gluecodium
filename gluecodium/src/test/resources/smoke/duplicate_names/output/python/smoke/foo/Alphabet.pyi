

import typing

from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    ALPHA = generated.smoke_foo_Alphabet.ALPHA
    BETA = generated.smoke_foo_Alphabet.BETA
    GAMMA = generated.smoke_foo_Alphabet.GAMMA

    @property
    def _native(self):
        return self.value

