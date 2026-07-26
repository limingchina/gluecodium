

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
#include "smoke/EnumWithAlias.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumWithAlias = ::smoke::EnumWithAlias;

void register_smoke_EnumWithAlias(py::module_& module) {
    py::enum_<EnumWithAlias>(module, "smoke_EnumWithAlias")
        .value("ONE", EnumWithAlias::ONE)
        .value("TWO", EnumWithAlias::TWO)
        .value("THREE", EnumWithAlias::THREE)
        .value("FIRST", EnumWithAlias::FIRST)
        .value("THE_BEST", EnumWithAlias::THE_BEST)
        ;
}

