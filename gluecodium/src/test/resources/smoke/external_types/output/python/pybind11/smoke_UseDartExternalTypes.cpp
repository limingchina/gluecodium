

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CompressionState.h"
#include "smoke/DartColor.h"
#include "smoke/DartSeason.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalTypes.h"

void register_UseDartExternalTypes(py::module_& module) {
    py::class_<UseDartExternalTypes>(module, "UseDartExternalTypes")
        .def("rectangle_round_trip", &UseDartExternalTypes::rectangle_round_trip, py::arg("input"))
        .def("compression_state_round_trip", &UseDartExternalTypes::compression_state_round_trip, py::arg("input"))
        .def("color_round_trip", &UseDartExternalTypes::color_round_trip, py::arg("input"))
        .def("season_round_trip", &UseDartExternalTypes::season_round_trip, py::arg("input"))
        ;
}

