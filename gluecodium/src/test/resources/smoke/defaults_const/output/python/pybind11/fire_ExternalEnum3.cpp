

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
#include "foo/AlienEnum3.h"




void register_fire_ExternalEnum3(py::module_& module) {
auto cls_ExternalEnum3 = py::enum_<foo::AlienEnum3>(module, "fire_ExternalEnum3")
        .value("ENABLED", foo::AlienEnum3::ENABLED)
        .value("DISABLED", foo::AlienEnum3::DISABLED)
        ;


}
