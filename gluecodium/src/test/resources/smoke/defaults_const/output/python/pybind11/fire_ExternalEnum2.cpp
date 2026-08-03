

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
#include "foo/AlienEnum2.h"




void register_fire_ExternalEnum2(py::module_& module) {
auto cls_ExternalEnum2 = py::enum_<foo::AlienEnum2>(module, "fire_ExternalEnum2")
        .value("ENABLED", foo::AlienEnum2::ENABLED)
        .value("DISABLED", foo::AlienEnum2::DISABLED)
        ;


}
