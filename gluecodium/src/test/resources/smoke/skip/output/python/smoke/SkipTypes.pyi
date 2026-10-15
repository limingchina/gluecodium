

from enum import Enum
import typing
from typing import Optional

class SkipTypes:

    class NotInJava:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, foo_field: str) -> None: ...

        foo_field: str



    class NotInSwift:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, foo_field: str) -> None: ...

        foo_field: str



    class NotInDart:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, foo_field: str) -> None: ...

        foo_field: str



    class NotInKotlin:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, foo_field: str) -> None: ...

        foo_field: str
