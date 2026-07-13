

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum1.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Enum1 = ::gluecodium::fire::Enum1;

void register_Enum1(py::module_& module) {
    py::enum_<Enum1>(module, "Enum1")
        .value("ENABLED", Enum1::ENABLED)
        .value("DISABLED", Enum1::DISABLED)
        ;
}

