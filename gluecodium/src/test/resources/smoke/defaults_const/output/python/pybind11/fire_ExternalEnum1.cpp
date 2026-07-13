

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum1.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExternalEnum1 = ::gluecodium::fire::ExternalEnum1;

void register_ExternalEnum1(py::module_& module) {
    py::enum_<foo::AlienEnum1>(module, "ExternalEnum1")
        .value("ENABLED", foo::AlienEnum1::ENABLED)
        .value("DISABLED", foo::AlienEnum1::DISABLED)
        ;
}

