

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartSeason.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartSeason = ::smoke::DartSeason;

void register_DartSeason(py::module_& module) {
    py::enum_<DartSeason>(module, "DartSeason")
        .value("WINTER", DartSeason::WINTER)
        .value("SPRING", DartSeason::SPRING)
        .value("SUMMER", DartSeason::SUMMER)
        .value("AUTUMN", DartSeason::AUTUMN)
        ;
}

