

from enum import Enum
import typing
from typing import Optional

class StructWithJavaPositionalDefaults:
    """Foo Bar this is a comment"""
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, first_free_field: str, second_free_field: bool) -> None: ...
    @typing.overload
    def __init__(self, first_init_field: int, first_free_field: str, second_init_field: float, second_free_field: bool, third_init_field: str) -> None: ...

    #: first init!
    first_init_field: int

    #: first free!
    first_free_field: str

    #: second init yeah!
    second_init_field: float

    #: second free here!
    second_free_field: bool

    #: third should be last!
    third_init_field: str
