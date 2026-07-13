

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/AttributesStruct.h"
#include "string"

void register_AttributesStruct(py::module_& module) {
    py::class_<AttributesStruct>(module, "AttributesStruct")
        .def_readwrite("field", &AttributesStruct::field)
        .def("very_fun", &AttributesStruct::very_fun, py::arg("param"))
        ;
}

