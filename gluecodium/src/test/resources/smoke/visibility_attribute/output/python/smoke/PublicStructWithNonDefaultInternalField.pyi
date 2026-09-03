

from enum import Enum
import typing

class PublicStructWithNonDefaultInternalField:

    defaulted_field: int

    _internal_field: str

    public_field: bool


