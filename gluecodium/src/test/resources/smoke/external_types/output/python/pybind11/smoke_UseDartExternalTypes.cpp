

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
#include "smoke/CompressionState.h"
#include "smoke/DartColor.h"
#include "smoke/DartSeason.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalTypes.h"

using UseDartExternalTypes = ::smoke::UseDartExternalTypes;



void register_smoke_UseDartExternalTypes(py::module_& module) {
auto cls_UseDartExternalTypes = py::class_<UseDartExternalTypes, std::shared_ptr<UseDartExternalTypes>>(module, "smoke_UseDartExternalTypes")
        .def("__gluecodium_id__", [](const UseDartExternalTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("rectangle_round_trip", &UseDartExternalTypes::rectangle_round_trip, py::arg("input"))
        .def_static("compression_state_round_trip", &UseDartExternalTypes::compression_state_round_trip, py::arg("input"))
        .def_static("color_round_trip", &UseDartExternalTypes::color_round_trip, py::arg("input"))
        .def_static("season_round_trip", &UseDartExternalTypes::season_round_trip, py::arg("input"))
        ;


}
