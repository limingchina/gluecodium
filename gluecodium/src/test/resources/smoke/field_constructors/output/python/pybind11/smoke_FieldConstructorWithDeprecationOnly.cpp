

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithDeprecationOnly.h"
#include "string"

void register_FieldConstructorWithDeprecationOnly(py::module_& module) {
    py::class_<FieldConstructorWithDeprecationOnly>(module, "FieldConstructorWithDeprecationOnly")
        .def_readwrite("string_field", &FieldConstructorWithDeprecationOnly::string_field)
        ;
}

