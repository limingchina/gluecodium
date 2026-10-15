

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
from smoke.EnumWrapper import EnumWrapper
from enum import Enum
import typing
from typing import Optional

class EnumDefaultsExternal:

    class SimpleEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field: ExternalEnum1) -> None: ...

        enum_field: ExternalEnum1



    class NullableEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field1: Optional[ExternalEnum2], enum_field2: Optional[ExternalEnum2]) -> None: ...

        enum_field1: Optional[ExternalEnum2]

        enum_field2: Optional[ExternalEnum2]



    class AliasEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, enum_field: ExternalEnum3) -> None: ...

        enum_field: ExternalEnum3



    class WrappedEnum:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, struct_field: EnumWrapper) -> None: ...

        struct_field: EnumWrapper



    EnumAlias = ExternalEnum3
