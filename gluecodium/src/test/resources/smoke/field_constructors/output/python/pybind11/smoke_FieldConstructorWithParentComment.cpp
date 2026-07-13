

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithParentComment.h"
#include "string"

void register_FieldConstructorWithParentComment(py::module_& module) {
    py::class_<FieldConstructorWithParentComment>(module, "FieldConstructorWithParentComment")
        .def_readwrite("string_field", &FieldConstructorWithParentComment::string_field)
        ;
}

