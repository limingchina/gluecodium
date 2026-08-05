

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
#include "smoke/FieldConstructorsWithLabels.h"
#include "cstdint"
#include "string"

using FieldConstructorsWithLabels = ::smoke::FieldConstructorsWithLabels;



void register_smoke_FieldConstructorsWithLabels(py::module_& module) {
auto cls_FieldConstructorsWithLabels = py::class_<FieldConstructorsWithLabels>(module, "smoke_FieldConstructorsWithLabels")
        .def_readwrite("string_field", &FieldConstructorsWithLabels::string_field)
        .def_readwrite("int_field", &FieldConstructorsWithLabels::int_field)
        .def_readwrite("bool_field", &FieldConstructorsWithLabels::bool_field)
        .def(py::init<>())
        .def(py::init<int32_t, bool>(), py::arg("int_field"), py::arg("bool_field"))
        .def(py::init<::std::string, int32_t, bool>(), py::arg("string_field"), py::arg("int_field"), py::arg("bool_field"))
        ;


}
