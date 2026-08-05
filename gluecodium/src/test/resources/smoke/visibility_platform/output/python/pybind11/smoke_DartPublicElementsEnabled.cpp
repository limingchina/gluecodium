

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
#include "smoke/DartPublicElementsEnabled.h"
#include "string"

using DartPublicElementsEnabled = ::smoke::DartPublicElementsEnabled;



void register_smoke_DartPublicElementsEnabled(py::module_& module) {
auto cls_DartPublicElementsEnabled = py::class_<DartPublicElementsEnabled>(module, "smoke_DartPublicElementsEnabled")
        .def_readwrite("bool_field", &DartPublicElementsEnabled::bool_field)
        .def_readwrite("_string_field", &DartPublicElementsEnabled::string_field)
        .def(py::init<>())
        .def(py::init([](const bool& bool_field) {
            return DartPublicElementsEnabled(bool_field, ::std::string{});
        }), py::arg("bool_field"))
        .def("_foo", &DartPublicElementsEnabled::foo)
        ;


}
