

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DateInterval.h"
#include "smoke/Persistence.h"
#include "smoke/PseudoColor.h"
#include "smoke/SwiftSeason.h"
#include "smoke/UseSwiftExternalTypes.h"

void register_UseSwiftExternalTypes(py::module_& module) {
    py::class_<UseSwiftExternalTypes>(module, "UseSwiftExternalTypes")
        .def("date_interval_round_trip", &UseSwiftExternalTypes::date_interval_round_trip, py::arg("input"))
        .def("persistence_round_trip", &UseSwiftExternalTypes::persistence_round_trip, py::arg("input"))
        .def("color_round_trip", &UseSwiftExternalTypes::color_round_trip, py::arg("input"))
        .def("season_round_trip", &UseSwiftExternalTypes::season_round_trip, py::arg("input"))
        ;
}

