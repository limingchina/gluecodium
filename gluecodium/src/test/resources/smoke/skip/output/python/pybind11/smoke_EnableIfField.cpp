

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
#include "smoke/EnableIfField.h"
#include "cstdint"
#include "string"

using EnableIfField = ::smoke::EnableIfField;



void register_smoke_EnableIfField(py::module_& module) {
auto cls_EnableIfField = py::class_<EnableIfField>(module, "smoke_EnableIfField")
        .def_readwrite("int_field", &EnableIfField::int_field)
        .def_readwrite("bool_field", &EnableIfField::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string, bool>(), py::arg("int_field"), py::arg("string_field"), py::arg("bool_field"))
        ;


}
