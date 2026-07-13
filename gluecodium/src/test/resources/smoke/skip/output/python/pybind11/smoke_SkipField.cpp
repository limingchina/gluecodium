

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipField.h"
#include "string"

void register_SkipField(py::module_& module) {
    py::class_<SkipField>(module, "SkipField")
        .def_readwrite("field", &SkipField::field)
        ;
}

