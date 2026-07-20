

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EnableIfTypesEnabled.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnableMeToo = ::smoke::EnableIfTypesEnabled::EnableMeToo;

void register_EnableIfTypesEnabledEnableMeToo(py::module_& module) {
    py::class_<EnableMeToo>(module, "EnableIfTypesEnabledEnableMeToo")
        .def_readwrite("field", &EnableMeToo::field)
        .def(py::init<>())
        .def(py::init<::smoke::EnableIfTypesEnabled::EnableMe>(), py::arg("field"))
        ;
}

