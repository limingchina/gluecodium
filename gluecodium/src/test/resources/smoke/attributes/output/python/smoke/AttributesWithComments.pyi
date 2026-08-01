

from enum import Enum
import typing

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

    #: Const comment
    PI = False

    class SomeStruct:
    
        #: Field comment
        field: str
    
    

