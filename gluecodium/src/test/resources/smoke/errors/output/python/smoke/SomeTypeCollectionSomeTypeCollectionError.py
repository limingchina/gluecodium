

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class SomeTypeCollectionSomeTypeCollectionError(Enum):

    ERROR_A = generated.smoke_SomeTypeCollectionSomeTypeCollectionError.ERROR_A
    ERROR_B = generated.smoke_SomeTypeCollectionSomeTypeCollectionError.ERROR_B

    @property
    def _native(self):
        return self.value

