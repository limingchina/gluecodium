

import typing

from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    A = generated.smoke_Alphabet.A
    B = generated.smoke_Alphabet.B
    C = generated.smoke_Alphabet.C

    @property
    def _native(self):
        return self.value

