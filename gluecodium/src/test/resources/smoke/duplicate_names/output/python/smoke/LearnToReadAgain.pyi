

from smoke.bar.Alphabet import Alphabet as smoke_bar_Alphabet
from smoke.foo.Alphabet import Alphabet as smoke_foo_Alphabet
from enum import Enum
import typing
from typing import Optional

class LearnToReadAgain:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, field_b: smoke_foo_Alphabet, field_c: smoke_bar_Alphabet) -> None: ...

    field_b: smoke_foo_Alphabet

    field_c: smoke_bar_Alphabet
