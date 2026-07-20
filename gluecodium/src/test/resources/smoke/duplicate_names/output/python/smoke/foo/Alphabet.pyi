

import typing

from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    ALPHA = generated.Alphabet.ALPHA
    BETA = generated.Alphabet.BETA
    GAMMA = generated.Alphabet.GAMMA

    @property
    def _native(self):
        return self.value

