

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsAllDefaults.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsAllDefaults(py::module_& module) {
    py::class_<FieldConstructorsAllDefaults>(module, "FieldConstructorsAllDefaults")
        .def_readwrite("string_field", &FieldConstructorsAllDefaults::string_field)
        .def_readwrite("int_field", &FieldConstructorsAllDefaults::int_field)
        .def_readwrite("bool_field", &FieldConstructorsAllDefaults::bool_field)
        ;
}

