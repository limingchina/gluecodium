

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
#include "smoke/Season.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Season = ::smoke::Season;

void register_smoke_Season(py::module_& module) {
    py::enum_<Season>(module, "smoke_Season")
        .value("WINTER", Season::WINTER)
        .value("SPRING", Season::SPRING)
        .value("SUMMER", Season::SUMMER)
        .value("AUTUMN", Season::AUTUMN)
        ;
}

