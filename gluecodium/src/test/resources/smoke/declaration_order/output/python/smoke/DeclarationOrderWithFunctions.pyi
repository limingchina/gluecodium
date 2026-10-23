

from enum import Enum
import typing
from typing import Optional

class DeclarationOrderWithFunctions:
    def __init__(self) -> None: ...

    class MainStructWithFunctions:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, struct_field: DeclarationOrderWithFunctions.FieldStruct) -> None: ...

        struct_field: DeclarationOrderWithFunctions.FieldStruct

        def with_parameter(self, input: DeclarationOrderWithFunctions.ParameterStruct):
            ...

        def with_return(self) -> DeclarationOrderWithFunctions.ReturnStruct:
            ...

        def with_thrown(self):
            ...



    class FieldStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class ParameterStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class ReturnStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class ThrownStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: str) -> None: ...

        some_field: str



    class FooBarError(Exception):
        message: str

        def __init__(self, message: str) -> None: ...
