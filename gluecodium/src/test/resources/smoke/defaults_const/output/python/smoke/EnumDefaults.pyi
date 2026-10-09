

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
from smoke.EnumWrapper import EnumWrapper
from enum import Enum
import typing
from typing import Optional

class EnumDefaults:

    class SimpleEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field: Enum1) -> None: ...

        enum_field: Enum1



    class NullableEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field1: Optional[Enum2], enum_field1: Optional[Enum2]) -> None: ...

        enum_field1: Optional[Enum2]

        enum_field1: Optional[Enum2]



    class AliasEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field: Enum3) -> None: ...

        enum_field: Enum3



    class WrappedEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, struct_field: EnumWrapper) -> None: ...

        struct_field: EnumWrapper



    EnumAlias = Enum3
