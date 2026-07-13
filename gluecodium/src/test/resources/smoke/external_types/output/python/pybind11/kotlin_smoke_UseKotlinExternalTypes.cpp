

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "kotlin_smoke/Currency.h"
#include "kotlin_smoke/KotlinExternalTypesStruct.h"
#include "kotlin_smoke/Month.h"
#include "kotlin_smoke/Season.h"
#include "kotlin_smoke/SystemColor.h"
#include "kotlin_smoke/TimeZone.h"
#include "kotlin_smoke/UseKotlinExternalTypes.h"
#include "kotlin_smoke/VeryBoolean.h"

void register_UseKotlinExternalTypes(py::module_& module) {
    py::class_<UseKotlinExternalTypes>(module, "UseKotlinExternalTypes")
        .def("currency_round_trip", &UseKotlinExternalTypes::currency_round_trip, py::arg("input"))
        .def("time_zone_round_trip", &UseKotlinExternalTypes::time_zone_round_trip, py::arg("input"))
        .def("month_round_trip", &UseKotlinExternalTypes::month_round_trip, py::arg("input"))
        .def("color_round_trip", &UseKotlinExternalTypes::color_round_trip, py::arg("input"))
        .def("season_round_trip", &UseKotlinExternalTypes::season_round_trip, py::arg("input"))
        .def("struct_round_trip", &UseKotlinExternalTypes::struct_round_trip, py::arg("input"))
        .def("very_boolean_unbox", &UseKotlinExternalTypes::very_boolean_unbox, py::arg("input"))
        ;
}

