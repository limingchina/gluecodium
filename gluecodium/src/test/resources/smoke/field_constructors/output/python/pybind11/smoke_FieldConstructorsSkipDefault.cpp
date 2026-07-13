

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsSkipDefault.h"
#include "cstdint"
#include "string"

void register_FieldConstructorsSkipDefault(py::module_& module) {
    py::class_<FieldConstructorsSkipDefault>(module, "FieldConstructorsSkipDefault")
        .def_readwrite("string_field", &FieldConstructorsSkipDefault::string_field)
        .def_readwrite("int_field", &FieldConstructorsSkipDefault::int_field)
        ;
}

