

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsSkipCpp.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsSkipCpp(py::module_& module) {
    py::class_<FieldConstructorsSkipCpp>(module, "FieldConstructorsSkipCpp")
        .def_readwrite("string_field", &FieldConstructorsSkipCpp::string_field)
        .def_readwrite("int_field", &FieldConstructorsSkipCpp::int_field)
        ;
}

