

from enum import Enum
import typing
from typing import Optional

class CommentsTypeCollection:
    def __init__(self) -> None: ...

    class TypeCollectionStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, field: int) -> None: ...

        field: int



    class TypeCollectionEnum(Enum):

        ITEM = 0



    TypeCollectionTypedef = bool



    TYPE_COLLECTION_CONSTANT = True
