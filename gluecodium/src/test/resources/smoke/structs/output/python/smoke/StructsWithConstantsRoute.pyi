

from smoke.RouteUtilsRouteType import RouteUtilsRouteType
import typing


from _native_base import _NativeBase

import generated


class StructsWithConstantsRoute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithConstantsRoute):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithConstantsRoute(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def description(self) -> str:
        """"""
        return self._native.description
    @description.setter
    def description(self, value: str):
      self._native.description = getattr(value, "_native", value)



    @property
    def type(self) -> RouteUtilsRouteType:
        """"""
        return RouteUtilsRouteType(self._native.type)
    @type.setter
    def type(self, value: RouteUtilsRouteType):
      self._native.type = getattr(value, "_native", value)



    DEFAULT_DESCRIPTION = "Nonsense"


    DEFAULT_TYPE = RouteType.EQUESTRIAN

