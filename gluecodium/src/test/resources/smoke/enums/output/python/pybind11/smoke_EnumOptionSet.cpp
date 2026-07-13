

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnumOptionSet.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumOptionSet = ::smoke::EnumOptionSet;

void register_EnumOptionSet(py::module_& module) {
    py::enum_<EnumOptionSet>(module, "EnumOptionSet")
        .value("ONE", EnumOptionSet::ONE)
        .value("TWO", EnumOptionSet::TWO)
        .value("THREE", EnumOptionSet::THREE)
        ;
}

