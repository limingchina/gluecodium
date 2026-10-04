

from smoke.Alphabet import Alphabet as smoke_Alphabet
from smoke.foo.Alphabet import Alphabet as smoke_foo_Alphabet
from enum import Enum
import typing
from typing import Optional

class NameClashLists:

    field_a: list[smoke_Alphabet]

    field_b: list[smoke_foo_Alphabet]
