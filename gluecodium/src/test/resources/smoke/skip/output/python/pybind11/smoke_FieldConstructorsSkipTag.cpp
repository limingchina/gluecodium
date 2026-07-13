

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/FieldConstructorsSkipTag.h"
#include "string"

void register_FieldConstructorsSkipTag(py::module_& module) {
    py::class_<FieldConstructorsSkipTag>(module, "FieldConstructorsSkipTag")
        .def_readwrite("field1", &FieldConstructorsSkipTag::field1)
        ;
}

