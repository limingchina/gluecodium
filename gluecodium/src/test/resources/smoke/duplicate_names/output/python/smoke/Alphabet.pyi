

import typing

from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    A = generated.Alphabet.A
    B = generated.Alphabet.B
    C = generated.Alphabet.C

    @property
    def _native(self):
        return self.value

