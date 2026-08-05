

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "fire/Enum1.h"

using Enum1 = ::fire::Enum1;



void register_fire_Enum1(py::module_& module) {
auto cls_Enum1 = py::enum_<Enum1>(module, "fire_Enum1")
        .value("ENABLED", Enum1::ENABLED)
        .value("DISABLED", Enum1::DISABLED)
        ;


}
