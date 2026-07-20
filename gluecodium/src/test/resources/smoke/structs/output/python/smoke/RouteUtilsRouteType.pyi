

import typing

from enum import Enum

import generated


class RouteUtilsRouteType(Enum):
    """"""

    NONE = generated.RouteUtilsRouteType.NONE
    CAR = generated.RouteUtilsRouteType.CAR
    PEDESTRIAN = generated.RouteUtilsRouteType.PEDESTRIAN
    EQUESTRIAN = generated.RouteUtilsRouteType.EQUESTRIAN

    @property
    def _native(self):
        return self.value

