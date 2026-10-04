

from smoke.ImmutableStructNoClash import ImmutableStructNoClash
from enum import Enum
import typing
from typing import Optional

class MutableStructImmutableFields:

    struct_field: ImmutableStructNoClash

    int_field: int

    bool_field: bool
