

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
#include "smoke/FieldConstructorsParameterDefaults.h"
#include "cstdint"
#include "string"

using FieldConstructorsParameterDefaults = ::smoke::FieldConstructorsParameterDefaults;



void register_smoke_FieldConstructorsParameterDefaults(py::module_& module) {
auto cls_FieldConstructorsParameterDefaults = py::class_<FieldConstructorsParameterDefaults>(module, "smoke_FieldConstructorsParameterDefaults")
        .def_readwrite("string_field", &FieldConstructorsParameterDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsParameterDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsParameterDefaults::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t>(), py::arg("int_field"))
        .def(py::init<int32_t, bool>(), py::arg("int_field"), py::arg("bool_field"))
        .def(py::init<::std::string, int32_t, bool>(), py::arg("string_field"), py::arg("int_field"), py::arg("bool_field"))
        ;


}
