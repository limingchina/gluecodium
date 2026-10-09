

from enum import Enum
import typing
from typing import Optional

class OuterStructWithFieldConstructor:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, outer_struct_field: OuterStructWithFieldConstructor.InnerStructWithDefaults) -> None: ...

    outer_struct_field: OuterStructWithFieldConstructor.InnerStructWithDefaults

    class InnerStructWithDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, inner_struct_field: float) -> None: ...

        inner_struct_field: float
