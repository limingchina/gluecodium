

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum4.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Enum4 = ::gluecodium::fire::Enum4;

void register_Enum4(py::module_& module) {
    py::enum_<Enum4>(module, "Enum4")
        .value("ENABLED", Enum4::ENABLED)
        .value("DISABLED", Enum4::DISABLED)
        ;
}

