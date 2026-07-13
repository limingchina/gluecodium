

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NestedReferences.h"
#include "memory"
#include "string"

void register_NestedReferences(py::module_& module) {
    py::class_<NestedReferences>(module, "NestedReferences")
        .def("inside_out", &NestedReferences::inside_out, py::arg("struct1"), py::arg("struct2"))
        ;
}

