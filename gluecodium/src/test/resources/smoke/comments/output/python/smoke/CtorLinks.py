

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.CtorLinksOverloadedCtors import CtorLinksOverloadedCtors
from smoke.CtorLinksSingleCtor import CtorLinksSingleCtor
from smoke.CtorLinksSingleCtorWithOneArgument import CtorLinksSingleCtorWithOneArgument
from smoke.CtorLinksSingleCtorWithTwoArgument import CtorLinksSingleCtorWithTwoArgument

from _native_base import _NativeBase

import generated


class CtorLinks(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

