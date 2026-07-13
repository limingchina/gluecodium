

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorWithBothComments.h"
#include "string"

void register_FieldConstructorWithBothComments(py::module_& module) {
    py::class_<FieldConstructorWithBothComments>(module, "FieldConstructorWithBothComments")
        .def_readwrite("string_field", &FieldConstructorWithBothComments::string_field)
        ;
}

