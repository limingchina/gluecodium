

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
#include "smoke/FieldConstructorsAllDefaults.h"
#include "cstdint"
#include "string"

using FieldConstructorsAllDefaults = ::smoke::FieldConstructorsAllDefaults;



void register_smoke_FieldConstructorsAllDefaults(py::module_& module) {
auto cls_FieldConstructorsAllDefaults = py::class_<FieldConstructorsAllDefaults>(module, "smoke_FieldConstructorsAllDefaults")
        .def_readwrite("string_field", &FieldConstructorsAllDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsAllDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsAllDefaults::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        .def(py::init<int32_t, ::std::string>(), py::arg("int_field"), py::arg("string_field"))
        .def(py::init<bool, int32_t, ::std::string>(), py::arg("bool_field"), py::arg("int_field"), py::arg("string_field"))
        ;


}
