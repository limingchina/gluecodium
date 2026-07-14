

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/Currency.h"
#include "kotlin_smoke/KotlinExternalTypesStruct.h"
#include "kotlin_smoke/Month.h"
#include "kotlin_smoke/Season.h"
#include "kotlin_smoke/SystemColor.h"
#include "kotlin_smoke/TimeZone.h"
#include "kotlin_smoke/UseKotlinExternalTypes.h"
#include "kotlin_smoke/VeryBoolean.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseKotlinExternalTypes = ::kotlin_smoke::UseKotlinExternalTypes;

void register_UseKotlinExternalTypes(py::module_& module) {
    py::class_<UseKotlinExternalTypes, std::shared_ptr<UseKotlinExternalTypes>>(module, "UseKotlinExternalTypes")
        .def_static("currency_round_trip", &UseKotlinExternalTypes::currency_round_trip, py::arg("input"))
        .def_static("time_zone_round_trip", &UseKotlinExternalTypes::time_zone_round_trip, py::arg("input"))
        .def_static("month_round_trip", &UseKotlinExternalTypes::month_round_trip, py::arg("input"))
        .def_static("color_round_trip", &UseKotlinExternalTypes::color_round_trip, py::arg("input"))
        .def_static("season_round_trip", &UseKotlinExternalTypes::season_round_trip, py::arg("input"))
        .def_static("struct_round_trip", &UseKotlinExternalTypes::struct_round_trip, py::arg("input"))
        .def_static("very_boolean_unbox", &UseKotlinExternalTypes::very_boolean_unbox, py::arg("input"))
        ;
}

