

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
#include "smoke/FieldConstructorsSkipDefault.h"
#include "cstdint"
#include "string"

using FieldConstructorsSkipDefault = ::smoke::FieldConstructorsSkipDefault;



void register_smoke_FieldConstructorsSkipDefault(py::module_& module) {
auto cls_FieldConstructorsSkipDefault = py::class_<FieldConstructorsSkipDefault>(module, "smoke_FieldConstructorsSkipDefault")
        .def_readwrite("string_field", &FieldConstructorsSkipDefault::string_field)
        .def_readwrite("int_field", &FieldConstructorsSkipDefault::int_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
