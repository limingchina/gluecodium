

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
#include "smoke/Constants.h"

using Constants = ::smoke::Constants;
using StateEnum = ::smoke::Constants::StateEnum;



void register_smoke_Constants(py::module_& module) {
auto cls_Constants = py::class_<Constants>(module, "smoke_Constants")
        .def(py::init<>())
        ;

auto cls_ConstantsStateEnum = py::enum_<StateEnum>(cls_Constants, "StateEnum")
        .value("OFF", StateEnum::OFF)
        .value("ON", StateEnum::ON)
        ;


}
