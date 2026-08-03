

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
#include "smoke/SwiftSeason.h"

using SwiftSeason = ::smoke::SwiftSeason;



void register_smoke_SwiftSeason(py::module_& module) {
auto cls_SwiftSeason = py::enum_<SwiftSeason>(module, "smoke_SwiftSeason")
        .value("WINTER", SwiftSeason::WINTER)
        .value("SPRING", SwiftSeason::SPRING)
        .value("SUMMER", SwiftSeason::SUMMER)
        .value("AUTUMN", SwiftSeason::AUTUMN)
        ;


}
