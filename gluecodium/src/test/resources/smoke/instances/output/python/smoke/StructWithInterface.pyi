

from smoke.SimpleInterface import SimpleInterface
from enum import Enum
import typing
from typing import Optional

class StructWithInterface:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, interface_instance: SimpleInterface) -> None: ...

    interface_instance: SimpleInterface
