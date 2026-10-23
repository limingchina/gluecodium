

from smoke.JavaExternalCtor import JavaExternalCtor
from enum import Enum
import typing
from typing import Optional

class UseJavaExternalConst:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, string_field: str) -> None: ...

    string_field: str


    _DEFAULT_TRUTH = JavaExternalCtor("foo")
