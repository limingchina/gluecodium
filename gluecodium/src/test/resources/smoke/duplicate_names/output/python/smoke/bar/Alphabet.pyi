

import typing

from enum import Enum

import generated


class Alphabet(Enum):
    """"""

    ALEPH = generated.Alphabet.ALEPH
    BEIT = generated.Alphabet.BEIT
    GIMEL = generated.Alphabet.GIMEL

    @property
    def _native(self):
        return self.value

