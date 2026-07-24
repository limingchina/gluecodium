

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum2.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Enum2 = ::fire::Enum2;

void register_fire_Enum2(py::module_& module) {
    py::enum_<Enum2>(module, "Enum2")
        .value("ENABLED", Enum2::ENABLED)
        .value("DISABLED", Enum2::DISABLED)
        ;
}

