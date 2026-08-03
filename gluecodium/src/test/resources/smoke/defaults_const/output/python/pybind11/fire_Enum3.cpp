

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
#include "fire/Enum3.h"

using Enum3 = ::fire::Enum3;



void register_fire_Enum3(py::module_& module) {
auto cls_Enum3 = py::enum_<Enum3>(module, "fire_Enum3")
        .value("ENABLED", Enum3::ENABLED)
        .value("DISABLED", Enum3::DISABLED)
        ;


}
