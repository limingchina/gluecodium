

from smoke.DateInterval import DateInterval
from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor
from smoke.SwiftSeason import SwiftSeason

class UseSwiftExternalTypes:
    """"""

    def __init__(self, native):
        self._native = native


    def date_interval_round_trip(self, input: DateInterval) -> DateInterval:
        """"""
        return self._native.date_interval_round_trip(input)


    def persistence_round_trip(self, input: Persistence) -> Persistence:
        """"""
        return self._native.persistence_round_trip(input)


    def color_round_trip(self, input: PseudoColor) -> PseudoColor:
        """"""
        return self._native.color_round_trip(input)


    def season_round_trip(self, input: SwiftSeason) -> SwiftSeason:
        """"""
        return self._native.season_round_trip(input)

