

from enum import Enum
import typing
from typing import Optional

class AttributesWithComments:
    """Class comment"""

    def very_fun(self):
        """Function comment"""
        ...

    @property
    def prop(self) -> str:
        """Property comment"""
        ...

    @prop.setter
    def prop(self, value: str) -> None:
        """Setter comment"""
        ...

    class SomeStruct:

        #: Field comment
        field: str



    #: Const comment
    PI = False
