

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DateInterval.h"
#include "smoke/Persistence.h"
#include "smoke/PseudoColor.h"
#include "smoke/SwiftSeason.h"
#include "smoke/UseSwiftExternalTypes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseSwiftExternalTypes = ::gluecodium::smoke::UseSwiftExternalTypes;

void register_UseSwiftExternalTypes(py::module_& module) {
    py::class_<UseSwiftExternalTypes, std::shared_ptr<UseSwiftExternalTypes>>(module, "UseSwiftExternalTypes")
        .def("date_interval_round_trip", &UseSwiftExternalTypes::date_interval_round_trip, py::arg("input"))
        .def("persistence_round_trip", &UseSwiftExternalTypes::persistence_round_trip, py::arg("input"))
        .def("color_round_trip", &UseSwiftExternalTypes::color_round_trip, py::arg("input"))
        .def("season_round_trip", &UseSwiftExternalTypes::season_round_trip, py::arg("input"))
        ;
}

