

from smoke.Alphabet import Alphabet as smoke_Alphabet
from smoke.foo.Alphabet import Alphabet as smoke_foo_Alphabet
from enum import Enum
import typing
from typing import Optional

class LearnToRead:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field_a: smoke_Alphabet, field_b: smoke_foo_Alphabet) -> None: ...

    field_a: smoke_Alphabet

    field_b: smoke_foo_Alphabet
