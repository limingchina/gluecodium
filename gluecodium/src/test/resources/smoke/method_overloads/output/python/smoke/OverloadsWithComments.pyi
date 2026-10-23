

from enum import Enum
import typing
from typing import Optional

class OverloadsWithComments:

    @typing.overload
    def do_stuff(self):
        ...

    @typing.overload
    def do_stuff(self, stuff: str):
        """`OverloadsWithComments.do_stuff.stuff`"""
        ...
