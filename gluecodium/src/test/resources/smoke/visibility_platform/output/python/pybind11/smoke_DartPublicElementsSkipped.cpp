

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DartPublicElementsSkipped.h"

void register_DartPublicElementsSkipped(py::module_& module) {
    py::class_<DartPublicElementsSkipped>(module, "DartPublicElementsSkipped")
        .def_readwrite("bool_field", &DartPublicElementsSkipped::bool_field)
        .def_readwrite("string_field", &DartPublicElementsSkipped::string_field)
        .def("foo", &DartPublicElementsSkipped::foo)
        ;
}

