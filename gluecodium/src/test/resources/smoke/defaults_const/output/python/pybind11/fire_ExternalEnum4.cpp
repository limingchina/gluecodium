

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum4.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using foo::AlienEnum4 = foo::AlienEnum4;

void register_ExternalEnum4(py::module_& module) {
    py::enum_<foo::AlienEnum4>(module, "ExternalEnum4")
        .value("ENABLED", foo::AlienEnum4::ENABLED)
        .value("DISABLED", foo::AlienEnum4::DISABLED)
        ;
}

