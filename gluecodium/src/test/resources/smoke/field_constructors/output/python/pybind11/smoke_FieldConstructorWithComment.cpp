

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithComment.h"
#include "string"

void register_FieldConstructorWithComment(py::module_& module) {
    py::class_<FieldConstructorWithComment>(module, "FieldConstructorWithComment")
        .def_readwrite("string_field", &FieldConstructorWithComment::string_field)
        ;
}

