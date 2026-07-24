

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum4.h"


void register_fire_ExternalEnum4(py::module_& module) {
    py::enum_<foo::AlienEnum4>(module, "ExternalEnum4")
        .value("ENABLED", foo::AlienEnum4::ENABLED)
        .value("DISABLED", foo::AlienEnum4::DISABLED)
        ;
}

