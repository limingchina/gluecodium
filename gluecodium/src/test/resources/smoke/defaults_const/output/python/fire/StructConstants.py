

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from fire.SomeStruct import SomeStruct

from _native_base import _NativeBase

import generated


class StructConstants(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    DUMMY = {42}


    DUMMY2 = {11}


    DUMMY3 = StructConstants.DUMMY2


    DUMMY4 = {-1}


    DUMMY4 = {-2}

