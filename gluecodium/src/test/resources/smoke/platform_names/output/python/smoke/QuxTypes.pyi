

from enum import Enum
import typing
from typing import Optional

class QuxTypes:
    def __init__(self) -> None: ...

    class QuxStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, qux_field: str) -> None: ...

        qux_field: str

        @staticmethod
        def qux_make(qux_parameter: str) -> QuxTypes.QuxStruct:
            ...



    class QuxEnum(Enum):

        QUX_ITEM = 0



    QuxTypedef = float
