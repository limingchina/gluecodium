

from enum import Enum
import typing
from typing import Optional

class Structs:

    @staticmethod
    def get_external_struct() -> Structs.ExternalStruct:
        ...

    @staticmethod
    def get_another_external_struct() -> Structs.AnotherExternalStruct:
        ...

    class ExternalStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, string_field: str, external_string_field: str, external_array_field: list[int], external_struct_field: Structs.AnotherExternalStruct) -> None: ...

        string_field: str

        external_string_field: str

        external_array_field: list[int]

        external_struct_field: Structs.AnotherExternalStruct



    class AnotherExternalStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int_field: int) -> None: ...

        int_field: int
