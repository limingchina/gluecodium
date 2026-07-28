

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "dontsmoke/UseJavaExternalTypes.h"
#include "smoke/Currency.h"
#include "smoke/JavaExternalTypesStruct.h"
#include "smoke/Month.h"
#include "smoke/Season.h"
#include "smoke/SystemColor.h"
#include "smoke/TimeZone.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseJavaExternalTypes = ::dontsmoke::UseJavaExternalTypes;


void register_dontsmoke_UseJavaExternalTypes(py::module_& module) {
    py::class_<UseJavaExternalTypes, std::shared_ptr<UseJavaExternalTypes>>(module, "dontsmoke_UseJavaExternalTypes")
        .def("__gluecodium_id__", [](const UseJavaExternalTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("currency_round_trip", &UseJavaExternalTypes::currency_round_trip, py::arg("input"))
        .def_static("time_zone_round_trip", &UseJavaExternalTypes::time_zone_round_trip, py::arg("input"))
        .def_static("month_round_trip", &UseJavaExternalTypes::month_round_trip, py::arg("input"))
        .def_static("color_round_trip", &UseJavaExternalTypes::color_round_trip, py::arg("input"))
        .def_static("season_round_trip", &UseJavaExternalTypes::season_round_trip, py::arg("input"))
        .def_static("struct_round_trip", &UseJavaExternalTypes::struct_round_trip, py::arg("input"))
        ;
}

