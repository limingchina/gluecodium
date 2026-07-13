

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum3.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExternalEnum3 = ::gluecodium::fire::ExternalEnum3;

void register_ExternalEnum3(py::module_& module) {
    py::enum_<foo::AlienEnum3>(module, "ExternalEnum3")
        .value("ENABLED", foo::AlienEnum3::ENABLED)
        .value("DISABLED", foo::AlienEnum3::DISABLED)
        ;
}

