

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
#include "smoke/EnableIfTypesEnabled.h"

using EnableIfTypesEnabled = ::smoke::EnableIfTypesEnabled;
using EnableMeToo = ::smoke::EnableIfTypesEnabled::EnableMeToo;
using EnableMe = ::smoke::EnableIfTypesEnabled::EnableMe;



void register_smoke_EnableIfTypesEnabled(py::module_& module) {
auto cls_EnableIfTypesEnabled = py::class_<EnableIfTypesEnabled>(module, "smoke_EnableIfTypesEnabled")
        .def(py::init<>())
        ;

auto cls_EnableIfTypesEnabledEnableMeToo = py::class_<EnableMeToo>(cls_EnableIfTypesEnabled, "EnableMeToo")
        .def_readwrite("field", &EnableMeToo::field)
        .def(py::init<>())
        .def(py::init<::smoke::EnableIfTypesEnabled::EnableMe>(), py::arg("field"))
        ;

auto cls_EnableIfTypesEnabledEnableMe = py::enum_<EnableMe>(cls_EnableIfTypesEnabled, "EnableMe")
        .value("NOPE", EnableMe::NOPE)
        ;


}
