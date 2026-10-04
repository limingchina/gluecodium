

from enum import Enum
import typing
from typing import Optional

class JavaDeprecatedPosDefaultsCustom:
    """Foo Bar this is a comment"""
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, first_free_field: str) -> None: ...
    @typing.overload
    def __init__(self, first_init_field: int, first_free_field: str) -> None: ...

    #: first init!
    first_init_field: int

    #: first free!
    first_free_field: str

    @staticmethod
    def custom() -> JavaDeprecatedPosDefaultsCustom:
        ...
