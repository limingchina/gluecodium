

from __future__ import annotations


from enum import Enum

import generated


class SomeTypeCollectionSomeTypeCollectionError(Enum):
    """"""

    ERROR_A = generated.SomeTypeCollectionSomeTypeCollectionError.ERROR_A
    ERROR_B = generated.SomeTypeCollectionSomeTypeCollectionError.ERROR_B

    @property
    def _native(self):
        return self.value

