

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/AlienEnum1.h"


void register_fire_ExternalEnum1(py::module_& module) {
    py::enum_<foo::AlienEnum1>(module, "ExternalEnum1")
        .value("ENABLED", foo::AlienEnum1::ENABLED)
        .value("DISABLED", foo::AlienEnum1::DISABLED)
        ;
}

