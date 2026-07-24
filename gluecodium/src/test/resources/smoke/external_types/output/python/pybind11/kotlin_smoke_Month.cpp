

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "kotlin_smoke/Month.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Month = ::kotlin_smoke::Month;

void register_kotlin_smoke_Month(py::module_& module) {
    py::enum_<Month>(module, "Month")
        .value("JANUARY", Month::JANUARY)
        .value("FEBRUARY", Month::FEBRUARY)
        .value("MARCH", Month::MARCH)
        ;
}

