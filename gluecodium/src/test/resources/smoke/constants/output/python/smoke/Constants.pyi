

import typing


from _native_base import _NativeBase

import generated


class Constants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.Constants):
            super().__init__(args[0])
        else:
            super().__init__(generated.Constants(*[_unwrap(arg) for arg in args]))


    BOOL_CONSTANT = True


    INT_CONSTANT = -11


    UINT_CONSTANT = 4294967295


    FLOAT_CONSTANT = 2.71


    DOUBLE_CONSTANT = -3.14


    STRING_CONSTANT = "Foo bar"


    ENUM_CONSTANT = StateEnum.ON

