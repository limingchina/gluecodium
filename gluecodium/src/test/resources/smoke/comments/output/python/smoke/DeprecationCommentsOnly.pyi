

from enum import Enum
import typing
from typing import Optional

class DeprecationCommentsOnly:
    """"""

    def some_method_with_all_comments(self, input: str) -> bool:
        """"""
        ...

    @property
    def is_some_property(self) -> bool:
        """"""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        ...

    class SomeStruct:
        """"""
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field: bool) -> None: ...

        #:
        some_field: bool



    class SomeEnum(Enum):
        """"""

        USELESS = 0



    #:
    Usefulness = bool



    #:
    VERY_USEFUL = True
