

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnableIfField.h"
#include "cstdint"
#include "string"

void register_EnableIfField(py::module_& module) {
    py::class_<EnableIfField>(module, "EnableIfField")
        .def_readwrite("int_field", &EnableIfField::int_field)
        .def_readwrite("string_field", &EnableIfField::string_field)
        .def_readwrite("bool_field", &EnableIfField::bool_field)
        ;
}

