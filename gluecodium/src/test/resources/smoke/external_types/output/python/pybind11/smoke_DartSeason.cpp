

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartSeason.h"

using DartSeason = ::smoke::DartSeason;



void register_smoke_DartSeason(py::module_& module) {
auto cls_DartSeason = py::enum_<DartSeason>(module, "smoke_DartSeason")
        .value("WINTER", DartSeason::WINTER)
        .value("SPRING", DartSeason::SPRING)
        .value("SUMMER", DartSeason::SUMMER)
        .value("AUTUMN", DartSeason::AUTUMN)
        ;


}
