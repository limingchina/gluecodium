

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithDeprecationAndComment.h"
#include "string"

void register_FieldConstructorWithDeprecationAndComment(py::module_& module) {
    py::class_<FieldConstructorWithDeprecationAndComment>(module, "FieldConstructorWithDeprecationAndComment")
        .def_readwrite("string_field", &FieldConstructorWithDeprecationAndComment::string_field)
        ;
}

