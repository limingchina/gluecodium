

from smoke.LambdasDeclarationOrderSomeStruct import LambdasDeclarationOrderSomeStruct
from smoke.LambdasInterface import LambdasInterface
from smoke.LambdasWithStructuredTypesClassCallback import LambdasWithStructuredTypesClassCallback
from smoke.LambdasWithStructuredTypesStructCallback import LambdasWithStructuredTypesStructCallback
import typing
from typing import Callable

class LambdasWithStructuredTypes:

    def do_class_stuff(self, callback: Callable[[LambdasInterface], None]):
        ...

    def do_struct_stuff(self, callback: Callable[[LambdasDeclarationOrderSomeStruct], None]):
        ...

