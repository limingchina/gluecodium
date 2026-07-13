

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsWithLabels.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsWithLabels(py::module_& module) {
    py::class_<FieldConstructorsWithLabels>(module, "FieldConstructorsWithLabels")
        .def_readwrite("string_field", &FieldConstructorsWithLabels::string_field)
        .def_readwrite("int_field", &FieldConstructorsWithLabels::int_field)
        .def_readwrite("bool_field", &FieldConstructorsWithLabels::bool_field)
        ;
}

